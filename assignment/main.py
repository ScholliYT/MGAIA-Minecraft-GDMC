import numpy as np
from gdpc import Editor, Transform
from glm import ivec3

import assignment.bakery.bakery as bakery
import assignment.brickhouse.brickhouse as brickhouse
import assignment.farm.farm as farm
from assignment.buildarea.build_map import MapHolder
from assignment.buildarea.team import build_on_spot, compute_boxes

# Hyperparameter for finding building spaces
ACCEPTABLE_BUILDING_SCORE = 1.3


def build_brickhouses(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, count=3
):
    size_struct = 11
    print("Building houses...")
    for it in range(count):
        print("Fetching location to build")
        (loc_x, loc_y, loc_z, house_grid) = compute_boxes(
            ED,
            mymap,
            heights,
            it,
            start_x=startx,
            start_z=startz,
            acceptable_building_score=ACCEPTABLE_BUILDING_SCORE,
            size_struct=size_struct,
        )
        buildable = [[bool(x) for x in xs] for xs in house_grid]
        building_location = (
            ivec3(loc_x, loc_y - 1, loc_z)
            - ivec3(size_struct, 0, size_struct)
            - ivec3(int(size_struct / 2), 0, int(size_struct / 2))
        )
        building_size = (len(house_grid) + 2, 2, len(house_grid[0]) + 2)

        print("Generating building")
        wfc = brickhouse.random_building(size=building_size, buildable=buildable)
        building = brickhouse.wfc_state_to_minecraft_blocks(wfc.collapsed_state())

        # claim all used zones, i.e. ones that are not air blocks
        # some index shifts because of differend formats
        used_zones = [
            [
                int(building[-xi - 2][0][zi + 1][0].name != brickhouse.empty_space_air)
                for zi, zs in enumerate(xs)
            ]
            for xi, xs in enumerate(buildable)
        ]
        build_on_spot(
            ED, mymap, loc_x, loc_y, loc_z, used_zones, size_struct, build_grid_indicator=True
        )

        print("Building house at", building_location, "of size", building_size)
        with ED.pushTransform(Transform(translation=building_location)):
            # building = deterministic_building()
            brickhouse.build_brickhouse(editor=ED, building=building, place_air=False)


def build_bakeries(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, count=2
):
    size_struct = 7
    print("Building Bakeries...")
    for it in range(count):
        (loc_x, loc_y, loc_z, house_grid) = compute_boxes(
            ED,
            mymap,
            heights,
            it,
            start_x=startx,
            start_z=startz,
            acceptable_building_score=ACCEPTABLE_BUILDING_SCORE,
            size_struct=size_struct,
        )
        buildable = [[bool(x) for x in xs] for xs in house_grid]

        building_location = (
            ivec3(loc_x, loc_y, loc_z)
            - ivec3(size_struct, 0, size_struct)
            - ivec3(int(size_struct / 2), 0, int(size_struct / 2))
        )
        building_size = (len(house_grid) + 2, 1, len(house_grid[0]) + 2)
        print("Building bakery at", building_location, "of size", building_size)
        build_on_spot(
            ED, mymap, loc_x, loc_y, loc_z, house_grid, size_struct, build_grid_indicator=False
        )

        with ED.pushTransform(Transform(translation=building_location)):
            wfc = bakery.random_building(size=building_size, buildable=buildable)
            building = bakery.wfc_state_to_minecraft_blocks(wfc.collapsed_state())
            bakery.build_bakery(editor=ED, building=building, place_air=False)


def build_farms(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, count=2
):
    size_struct = 7
    print("Building farms...")
    for it in range(count):
        (loc_x, loc_y, loc_z, house_grid) = compute_boxes(
            ED,
            mymap,
            heights,
            it,
            start_x=startx,
            start_z=startz,
            acceptable_building_score=ACCEPTABLE_BUILDING_SCORE,
            size_struct=size_struct,
        )
        buildable = [[bool(x) for x in xs] for xs in house_grid]

        building_location = (
            ivec3(loc_x, loc_y, loc_z)
            - ivec3(size_struct, 0, size_struct)
            - ivec3(int(size_struct / 2), 0, int(size_struct / 2))
        )
        building_size = (len(house_grid) + 2, 1, len(house_grid[0]) + 2)
        print("Building farm at", building_location, "of size", building_size)
        build_on_spot(
            ED, mymap, loc_x, loc_y, loc_z, house_grid, size_struct, build_grid_indicator=False
        )

        with ED.pushTransform(Transform(translation=building_location)):
            wfc = farm.random_building(size=building_size, buildable=buildable)
            building = farm.wfc_state_to_minecraft_blocks(wfc.collapsed_state())
            farm.build_farm(editor=ED, building=building, place_air=False)


def main():
    ED = Editor(buffering=True)

    BUILD_AREA = ED.getBuildArea()  # BUILDAREA

    STARTX, _, STARTZ = BUILD_AREA.begin

    WORLDSLICE = ED.loadWorldSlice(BUILD_AREA.toRect(), cache=True)  # this takes a while
    heights = np.array(WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"])

    try:
        mymap = MapHolder(ED, heights, ACCEPTABLE_BUILDING_SCORE)
        print("Calculating heights and making Build Map...")
        mymap.find_flat_areas_and_trees(print_colors=False)

        build_brickhouses(mymap, ED, STARTX, STARTZ, heights)
        build_bakeries(mymap, ED, STARTX, STARTZ, heights, count=1)
        build_farms(mymap, ED, STARTX, STARTZ, heights)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
