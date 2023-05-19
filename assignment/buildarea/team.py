import logging
from typing import List

import numpy as np
from gdpc import Editor, Transform
from termcolor import colored

import assignment.buildarea.build_functions as build_funcs
import assignment.buildarea.helper as helper
from assignment.buildarea.build_map import MapHolder

logging.basicConfig(format=colored("%(name)s - %(levelname)s - %(message)s", color="yellow"))


def build_on_spot(
    editor: Editor,
    mymap: MapHolder,
    x_array: int,
    ystart: int,
    z_array: int,
    house_grid: List[List[int]],
    size_struct: int,
):
    xstart = x_array - int(size_struct / 2)
    zstart = z_array - int(size_struct / 2)

    for x in range(len(house_grid)):
        for z in range(len(house_grid[0])):
            if house_grid[x][z] == 1:
                # claim building spot, so no other building will be built there
                mymap.claim_zone(
                    xstart + x * size_struct,
                    zstart + z * size_struct,
                    size_struct,
                    size_struct,
                    "todo door",
                    "todo edges",
                )
                build_funcs.remove_trees(
                    editor, xstart, ystart, zstart, size_struct, size_struct, size_struct
                )
                # and remove trees first
                with editor.pushTransform(
                    Transform((xstart + x * size_struct, ystart, zstart + z * size_struct))
                ):
                    build_funcs.build_exterior_one_house_part(
                        editor, size_struct, size_struct, size_struct, 0, 1
                    )


# func that seeks location and orders to build a building over there,
# Make sure to built bigger buildings first(decrease size of buildings over time!!
def compute_boxes(
    editor: Editor,
    mymap: MapHolder,
    heights: np.ndarray,
    it: int,
    start_x: int,
    start_z: int,
    acceptable_building_score: float,
    size_struct: int,
):
    # find the best location to put a building
    best_loc_x, best_loc_z = helper.find_min_idx(mymap.block_slope_score, size_struct)
    # get the value of the minimum spot
    min_score = min([min(r) for r in mymap.block_slope_score])

    # see if this place is still suitable for a building
    if (min_score) > acceptable_building_score and it >= 1:
        return
    best_loc_y = heights[(best_loc_x, best_loc_z)]

    # If we are in a tree, go down untill we aren't
    while helper.is_tree(
        editor, start_x + best_loc_x, best_loc_y, start_z + best_loc_z
    ) or helper.is_air(editor, start_x + best_loc_x, best_loc_y, start_z + best_loc_z):
        best_loc_y -= 1

    # find all adjacent building spots
    x_array, z_array, house_grid = mymap.find_spot(best_loc_x, best_loc_y, best_loc_z, size_struct)

    return (start_x + x_array, best_loc_y, start_z + z_array, house_grid)


if __name__ == "__main__":
    ED = Editor(buffering=True)

    BUILD_AREA = ED.getBuildArea()  # BUILDAREA

    STARTX, _, STARTZ = BUILD_AREA.begin

    WORLDSLICE = ED.loadWorldSlice(BUILD_AREA.toRect(), cache=True)  # this takes a while
    heights = np.array(WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"])

    # Hypers for finding building spaces
    ACCEPTABLE_BUILDING_SCORE = 1.3
    size_struct = 7

    mymap = MapHolder(ED, heights, ACCEPTABLE_BUILDING_SCORE)
    print("calculating heights and making Build Map...")
    mymap.find_flat_areas_and_trees(print_colors=True)

    print("Building Houses...")
    for it in range(20):
        (loc_x, loc_y, loc_z, house_grid) = compute_boxes(
            ED,
            mymap,
            heights,
            it,
            start_x=STARTX,
            start_z=STARTZ,
            acceptable_building_score=ACCEPTABLE_BUILDING_SCORE,
            size_struct=size_struct,
        )
        build_on_spot(ED, mymap, loc_x, loc_y, loc_z, house_grid, size_struct)

        ED.flushBuffer()
