from types import ModuleType

import numpy as np
from gdpc import Editor, Transform
from glm import ivec3

import assignment.bakery.bakery as bakery
import assignment.brickhouse.brickhouse as brickhouse
import assignment.church.church as church
import assignment.farm.farm as farm
import assignment.school.school as school
from assignment.buildarea.build_map import MapHolder
from assignment.buildarea.team import build_on_spot, compute_boxes
from assignment.utils.not_buildable_exception import NotBuildableException

# Hyperparameter for finding building spaces
ACCEPTABLE_BUILDING_SCORE = 1.3


def build_building(
    building_module: ModuleType,
    size_struct: int,
    mymap: MapHolder,
    ED: Editor,
    startx: int,
    startz: int,
    offset: ivec3,
    heights: np.ndarray,
    building_no: int,
    wfc_height: int,
):
    print("Fetching location to build")
    (loc_x, loc_y, loc_z, house_grid) = compute_boxes(
        ED,
        mymap,
        heights,
        building_no,
        start_x=startx,
        start_z=startz,
        acceptable_building_score=ACCEPTABLE_BUILDING_SCORE,
        size_struct=size_struct,
    )
    buildable = [[bool(x) for x in xs] for xs in house_grid]
    building_location = (
        ivec3(loc_x, loc_y, loc_z)
        + offset
        - ivec3(size_struct, 0, size_struct)
        - ivec3(int(size_struct / 2), 0, int(size_struct / 2))
    )
    building_size = (len(house_grid) + 2, wfc_height, len(house_grid[0]) + 2)

    print("Generating building using WFC of size", building_size)
    try:
        wfc = building_module.random_building(size=building_size, buildable=buildable)
    except NotBuildableException:
        print(f"Failed to generate a building for location {building_no}. Skipping this")
        return
    building = building_module.wfc_state_to_minecraft_blocks(wfc.collapsed_state())

    # claim all used zones, i.e. ones that are not air blocks
    # some index shifts because of differend formats
    used_zones = [
        [
            int(building[-xi - 2][0][zi + 1][0].name != building_module.empty_space_air)
            for zi, zs in enumerate(xs)
        ]
        for xi, xs in enumerate(buildable)
    ]
    build_on_spot(
        ED, mymap, loc_x, loc_y, loc_z, used_zones, size_struct, build_grid_indicator=True
    )

    print("Placing building at", building_location, "of size", building_size)
    with ED.pushTransform(Transform(translation=building_location)):
        # building = deterministic_building()
        building_module.build(editor=ED, building=building, place_air=False)


def build_brickhouse(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, building_no: int
):
    print("Building Brickhouse")
    size_struct = 11
    wfc_height = 2
    offset = ivec3(0, -1, 0)
    build_building(
        building_module=brickhouse,
        size_struct=size_struct,
        mymap=mymap,
        ED=ED,
        startx=startx,
        startz=startz,
        offset=offset,
        heights=heights,
        building_no=building_no,
        wfc_height=wfc_height,
    )


def build_bakery(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, building_no: int
):
    print("Building Bakery")
    size_struct = 7
    wfc_height = 1
    offset = ivec3(0, 0, 0)
    build_building(
        building_module=bakery,
        size_struct=size_struct,
        mymap=mymap,
        ED=ED,
        startx=startx,
        startz=startz,
        offset=offset,
        heights=heights,
        building_no=building_no,
        wfc_height=wfc_height,
    )


def build_farm(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, building_no: int
):
    print("Building Farm")
    size_struct = 7
    wfc_height = 1
    offset = ivec3(0, 0, 0)
    build_building(
        building_module=farm,
        size_struct=size_struct,
        mymap=mymap,
        ED=ED,
        startx=startx,
        startz=startz,
        offset=offset,
        heights=heights,
        building_no=building_no,
        wfc_height=wfc_height,
    )


def build_church(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, building_no: int
):
    print("Building Church")
    size_struct = 11
    wfc_height = 1
    offset = ivec3(0, 0, 0)
    build_building(
        building_module=church,
        size_struct=size_struct,
        mymap=mymap,
        ED=ED,
        startx=startx,
        startz=startz,
        offset=offset,
        heights=heights,
        building_no=building_no,
        wfc_height=wfc_height,
    )


def build_school(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, building_no: int
):
    print("Building School")
    size_struct = 11
    wfc_height = 2
    offset = ivec3(0, 0, 0)
    build_building(
        building_module=school,
        size_struct=size_struct,
        mymap=mymap,
        ED=ED,
        startx=startx,
        startz=startz,
        offset=offset,
        heights=heights,
        building_no=building_no,
        wfc_height=wfc_height,
    )

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
        print("Build Map complete")

        for building_no in range(5):
            build_brickhouse(mymap, ED, STARTX, STARTZ, heights, building_no=building_no)
            build_church(mymap, ED, STARTX, STARTZ, heights, building_no=building_no)
            build_school(mymap, ED, STARTX, STARTZ, heights, building_no=building_no)
            build_bakery(mymap, ED, STARTX, STARTZ, heights, building_no=building_no)
            build_farm(mymap, ED, STARTX, STARTZ, heights, building_no=building_no)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
