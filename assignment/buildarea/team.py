import helper as helper
import build_functions as build_funcs
from build_map import MapHolder
import numpy as np


import logging

from termcolor import colored

from gdpc import Block, Editor, Transform


logging.basicConfig(format=colored("%(name)s - %(levelname)s - %(message)s", color="yellow"))

ED = Editor(buffering=True)

BUILD_AREA = ED.getBuildArea()  # BUILDAREA

STARTX, STARTY, STARTZ = BUILD_AREA.begin
LASTX, LASTY, LASTZ = BUILD_AREA.last
SIZEX, SIZEY, SIZEZ = BUILD_AREA.size
CENTERX = STARTX + (LASTX - STARTX) // 2
CENTERZ = STARTZ + (LASTZ - STARTZ) // 2

building_places = np.zeros((SIZEX, SIZEZ))

WORLDSLICE = ED.loadWorldSlice(BUILD_AREA.toRect(), cache=True)  # this takes a while
heights = np.array(WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"])

# Hypers for finding building spaces
ACCEPTABLE_BUILDING_SCORE = 1.3
Sigma = 3


def build_on_spot(Mymap,x_array,ystart,z_array, house_grid, size_struct):
    xstart = x_array - int(size_struct / 2)
    zstart = z_array - int(size_struct / 2)

    for x in range(len(house_grid)):
        for z in range(len(house_grid[0])):
            if house_grid[x][z] == 1:
                # claim building spot, so no other building will be built there
                Mymap.claim_zone(xstart+x*size_struct, zstart+z*size_struct, size_struct, size_struct, "todo door","todo edges")
                build_funcs.remove_trees(ED, xstart, ystart, zstart, size_struct, size_struct, size_struct)
                # and remove trees first
                with ED.pushTransform(Transform((xstart+x*size_struct, ystart, zstart+z*size_struct))):
                    build_funcs.build_exterior_one_house_part(ED, size_struct, size_struct, size_struct, 0, 1)

# func that seeks location and orders to build a building over there,
# Make sure to built bigger buildings first(decrease size of buildings over time!!
def build_boxes(Mymap, it):
    # size of building chunk
    size_struct = 7

    # find the best location to put a building
    best_loc_x, best_loc_z = helper.find_min_idx(Mymap.block_slope_score, size_struct)
    # get the value of the minimum spot
    min_score = min([min(r) for r in Mymap.block_slope_score])

    # see if this place is still suitable for a building
    if (min_score) > ACCEPTABLE_BUILDING_SCORE and it >= 1:
        return
    best_loc_y = heights[(best_loc_x, best_loc_z)]

    # If we are in a tree, go down untill we aren't
    while helper.is_tree(ED, STARTX + best_loc_x, best_loc_y, STARTZ + best_loc_z) or helper.is_air(ED, STARTX + best_loc_x, best_loc_y, STARTZ + best_loc_z):
        best_loc_y -= 1

    # find all adjacent building spots
    x_array, z_array, house_grid = Mymap.find_spot(best_loc_x, best_loc_y, best_loc_z, size_struct)
    # build building
    build_on_spot(Mymap,STARTX + x_array,best_loc_y,STARTZ + z_array, house_grid, size_struct)

if __name__ == '__main__':
    Mymap = MapHolder(ED,heights, ACCEPTABLE_BUILDING_SCORE)
    print("calculating heights and making Build Map...")
    Mymap.find_flat_areas_and_trees(print_colors=True)

    print("Building Houses...")
    for it in range(20):
        build_boxes(Mymap, it)
        ED.flushBuffer()
