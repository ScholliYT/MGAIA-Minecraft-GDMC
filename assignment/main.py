import numpy as np
from gdpc import Editor, Transform
from glm import ivec3

import assignment.brickhouse as brickhouse
from assignment.buildarea.build_map import MapHolder
from assignment.buildarea.team import build_on_spot, compute_boxes

# Hyperparameter for finding building spaces
ACCEPTABLE_BUILDING_SCORE = 1.3
size_struct = 11


def main():
    ED = Editor(buffering=True)

    BUILD_AREA = ED.getBuildArea()  # BUILDAREA

    STARTX, _, STARTZ = BUILD_AREA.begin

    WORLDSLICE = ED.loadWorldSlice(BUILD_AREA.toRect(), cache=True)  # this takes a while
    heights = np.array(WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"])

    try:
        mymap = MapHolder(ED, heights, ACCEPTABLE_BUILDING_SCORE)
        print("Calculating heights and making Build Map...")
        mymap.find_flat_areas_and_trees(print_colors=True)

        building_positions = []
        print("Building houses...")
        for it in range(5):
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
            building_positions.append((loc_x, loc_y, loc_z, house_grid))

            buildable = [[bool(x) for x in xs] for xs in house_grid]


            building_location = ivec3(loc_x, loc_y, loc_z) - ivec3(size_struct, 0, size_struct) - ivec3(int(size_struct/2), 0, int(size_struct/2))
            building_size = (len(house_grid)+2, 2, len(house_grid[0])+2)
            print("Building house at", building_location, "of size", building_size)
            build_on_spot(ED, mymap, loc_x, loc_y, loc_z, house_grid, size_struct)


            with ED.pushTransform(Transform(translation=building_location)):
                # building = deterministic_building()

                wfc = brickhouse.random_building(
                    size=building_size, buildable=buildable
                )
                building = brickhouse.wfc_state_to_minecraft_blocks(wfc.collapsed_state())
                brickhouse.build_brickhouse(editor=ED, building=building, place_air=False)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
