from types import ModuleType
from typing import List

import numpy as np
from gdpc import Block, Editor, Transform
from glm import ivec3
from tqdm import tqdm

import assignment.bakery.bakery as bakery
import assignment.brickhouse.brickhouse as brickhouse
import assignment.church.church as church
import assignment.farm.farm as farm
import assignment.school.school as school
from assignment.buildarea.build_map import MapHolder
from assignment.buildarea.helper import is_water
from assignment.buildarea.team import build_on_spot, compute_boxes
from assignment.narrator.narrator import place_narration_block
from assignment.pathing.water_real import make_paths
from assignment.utils.building_info import BuildingInfo
from assignment.utils.not_collapsable_exception import NotCollapsableException
from assignment.utils.wave_function_collaplse_util import print_state
from assignment.utils.wave_function_collapse import WaveFunctionCollapse

# Maximum number of buildings in the settlement
MAX_BUILDINGS = 20


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
    building_type: str,
) -> BuildingInfo | None:
    print("Fetching location to build")
    (loc_x, loc_y, loc_z, house_grid) = compute_boxes(
        ED,
        mymap,
        heights,
        start_x=startx,
        start_z=startz,
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
        wfc: WaveFunctionCollapse = building_module.random_building(size=building_size, buildable=buildable)
    except NotCollapsableException:
        print(f"Failed to generate a building for location {building_no}. Skipping this")
        return None

    print_state(wfc, "empty-space-air")
    building = building_module.wfc_state_to_minecraft_blocks(wfc.collapsed_state())

    # claim all used zones, i.e. ones that are not air blocks
    # some index shifts because of differend formats
    used_zones = [
        [
            int(building[-xi - 2][0][zi + 1][0].name != "empty-space-air") # building_module.empty_space_air does not work here because of paths in the name
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

    building_info = BuildingInfo(building_type=building_type)
    # locate all placed command blocks
    ED.updateWorldSlice()
    with ED.pushTransform(Transform(translation=building_location)):
        for x in range(building_size[0] * size_struct):
            for y in range(
                5
            ):  # 5 blocks should be sufficient to find a command block on almost ground level
                for z in range(building_size[2] * size_struct):
                    relative_offset = ivec3(x, y, z)
                    block = ED.getBlock(relative_offset)

                    if block.id == "minecraft:command_block":
                        command_block_location = building_location + relative_offset
                        building_info.command_block_locations.append(command_block_location)
    return building_info


def build_brickhouse(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, building_no: int
) -> BuildingInfo | None:
    print("Building Brickhouse")
    size_struct = 11
    wfc_height = 2
    offset = ivec3(0, -1, 0)
    return build_building(
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
        building_type="villager house",
    )


def build_bakery(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, building_no: int
) -> BuildingInfo | None:
    print("Building Bakery")
    size_struct = 7
    wfc_height = 1
    offset = ivec3(0, -1, 0)
    return build_building(
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
        building_type="bakery",
    )


def build_farm(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, building_no: int
) -> BuildingInfo | None:
    print("Building Farm")
    size_struct = 7
    wfc_height = 1
    offset = ivec3(0, -1, 0)
    return build_building(
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
        building_type="farm",
    )


def build_church(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, building_no: int
) -> BuildingInfo | None:
    print("Building Church")
    size_struct = 11
    wfc_height = 1
    offset = ivec3(0, 0, 0)
    return build_building(
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
        building_type="church",
    )


def build_school(
    mymap: MapHolder, ED: Editor, startx: int, startz: int, heights: np.ndarray, building_no: int
) -> BuildingInfo | None:
    print("Building School")
    size_struct = 11
    wfc_height = 2
    offset = ivec3(0, 0, 0)
    return build_building(
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
        building_type="school",
    )


def main():
    ED = Editor(buffering=True)

    BUILD_AREA = ED.getBuildArea()  # BUILDAREA

    STARTX, _, STARTZ = BUILD_AREA.begin

    WORLDSLICE = ED.loadWorldSlice(BUILD_AREA.toRect(), cache=True)  # this takes a while
    heightmap = np.array(WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"])

    try:
        print("Calculating heights and making Build Map...")
        mymap = MapHolder(ED, heightmap)
        mymap.find_flat_areas_and_trees(print_colors=False)
        map_block_slope_score = np.copy(mymap.block_slope_score)
        print("Build Map complete")

        building_infos: List[BuildingInfo] = []

        building_no = 0
        building_sucessful = True
        building_functions = (
            build_brickhouse,
            build_church,
            build_school,
            build_bakery,
            build_farm,
        )
        while building_no < MAX_BUILDINGS and building_sucessful:
            for bf in building_functions:
                building_info = bf(mymap, ED, STARTX, STARTZ, heightmap, building_no=building_no)

                if building_info is not None:
                    building_infos.append(building_info)
                    building_no += 1
                    building_sucessful = True
                else:
                    building_sucessful = False

        print("Information on buildings in the settlement", building_infos)

        print("Placing narration blocks for all buidling entrances...")
        for building_info in building_infos:
            for command_block_location in building_info.command_block_locations:
                place_narration_block(
                    ED, command_block_location, house_type=building_info.building_type
                )

        if sum([len(x.command_block_locations) for x in building_infos]) > 1:
            print("Generating paths to connect buildings with each other")
            # filter map for 20000
            filtered_building_map = np.zeros_like(mymap.building_places)
            filtered_building_map[mymap.building_places == 20_000] = 1

            # add positions of doors
            for building_info in building_infos:
                for command_block_location in building_info.command_block_locations:
                    relative_position = command_block_location - ivec3(STARTX, 0, STARTZ)
                    filtered_building_map[relative_position[0]][relative_position[2]] = 2

            final_paths = make_paths(slope=map_block_slope_score, building_map=filtered_building_map)

            print("Starting to build paths")
            ED.updateWorldSlice()
            for (x,z) in tqdm(list(zip(*np.where(final_paths == 1))), desc="Building paths"):
                global_position = ivec3(x, heightmap[x][z], z) + ivec3(STARTX, 0, STARTZ)

                if is_water(ED, global_position[0], global_position[1], global_position[2]):
                    ED.placeBlockGlobal(global_position, Block("oak_slab"))
                else:
                    ED.placeBlockGlobal(global_position + ivec3(0,-1,0), Block("gravel")) # Block("dirt_path")
        else:
            print("Not enough buildings to connect them with paths. At least 2 entrances are required.")


        ED.flushBuffer()
        print("Done with settlement generation!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
