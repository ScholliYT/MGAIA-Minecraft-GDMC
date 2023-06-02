# import sys
# import os

# parent_directory = r'C:\Users\sbone\Documents\Leiden Masters\YR1\SEM2\Modern Game AI Algorithms\Assignment 3\Bakery\MGAIA-Minecraft-GDMC-bakery'
# sys.path.append(os.path.abspath(parent_directory))


import pickle
import time
from typing import List, Tuple

from gdpc import Editor, Transform
from glm import ivec3
from tqdm import tqdm

import assignment.school.structure_adjacencies as sa
from assignment.school.structures import (
    empty_space_air,
    school_entrance,
    school_lower_stairs,
)
from assignment.utils.not_buildable_exception import NotBuildableException
from assignment.utils.structure import Structure, build_structure, load_structure
from assignment.utils.structure_adjacency import all_rotations, check_symmetry
from assignment.utils.structure_rotation import StructureRotation
from assignment.utils.wave_function_collaplse_util import (
    collapse_to_air_on_outer_rectangle,
    collapse_unbuildable_to_air,
    print_state,
)
from assignment.utils.wave_function_collapse import WaveFunctionCollapse


def structure_weights(structures: List[StructureRotation]):
    for s in structures:
        if s.structure_name == empty_space_air:
            yield 0.001
        else:
            yield 1.0


def random_building(
    size: Tuple[int, int, int] = (7, 1, 7), buildable: List[List[bool]] | None = None, max_retries=50
) -> WaveFunctionCollapse:
    wfc = WaveFunctionCollapse(size, sa.structure_adjecencies, structure_weights)
    if buildable is None:
        buildable = [
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
        ]

    def reinit():
        collapse_to_air_on_outer_rectangle(wfc, empty_space_air)

        print("Outer rectangle")
        print_state(wfc, air_name=empty_space_air)

        collapse_unbuildable_to_air(wfc, buildable, empty_space_air)

        print("Unbuildable")
        print_state(wfc, air_name=empty_space_air)

        # wfc.collapse_random_cell()
        wfc.collapse_random_cell()
        # wfc.collapse_random_cell()
        # wfc.collapse_random_cell()
        # wfc.collapse_random_cell()

        # wfc.collapse_cell_to_state([0,0,0], StructureRotation(empty_space_air, 0))
        # wfc.collapse_cell_to_state([3,0,3], StructureRotation(empty_space_air, 0))

        # wfc.collapse_cell_to_state([1,0,1], StructureRotation(brickhouse_entrance, 0))
        # wfc.collapse_cell_to_state([1,0,5], StructureRotation(brickhouse_entrance, 3))
        # wfc.collapse_cell_to_state([1,0,3], StructureRotation(brickhouse_middle, 3))
        # wfc.collapse_cell_to_state([1,0,4], StructureRotation(brickhouse_middle, 3))
        # wfc.collapse_cell_to_state([1,0,5], StructureRotation(brickhouse_middle, 3))

        # wfc.collapse_cell_to_state([5,0,5], StructureRotation(brickhouse_inner_corner_m2m, 0))
        # wfc.collapse_cell_to_state([13,0,13], StructureRotation(brickhouse_center, 0))

        # wfc.collapse_cell_to_state([4,0,4], StructureRotation(brickhouse_courtyard, 0))
        # wfc.collapse_cell_to_state([11,0,4], StructureRotation(brickhouse_courtyard, 0))

        # wfc.collapse_cell_to_state([1,1,3], StructureRotation(brickhouse_roofhouse_middle_to_flat, 0))

        # wfc.collapse_cell_to_state([6,0,6], StructureRotation(brickhouse_entrance, 2))

    def building_criterion_met(wfc: WaveFunctionCollapse):
        set(wfc.used_structures()).issubset(set([*all_rotations(empty_space_air)]))
        return any(
            [StructureRotation(school_entrance, r) in set(wfc.used_structures()) for r in range(4)]
        ) and any(
            [
                StructureRotation(school_lower_stairs, r) in set(wfc.used_structures())
                for r in range(4)
            ]
        )

        # return (not air_only) and contains_door
        # return True

    retries = wfc.collapse_with_retry(reinit=reinit)
    while not building_criterion_met(wfc) and retries < max_retries:   # used air structures only
        wfc._initialize_state_space_superposition()
        retries += 1 + wfc.collapse_with_retry(reinit=reinit)

    if retries >= max_retries:
        raise NotBuildableException()
    print(f"WFC collapsed after {retries} retries")
    return wfc


def wfc_state_to_minecraft_blocks(
    building: List[List[List[StructureRotation]]],
) -> List[List[List[Tuple[Structure, int]]]]:
    # transform StructuredRotation to (Structure,rotation) tuple
    buidling = [
        [[(load_structure(z.structure_name), z.rotation) for z in ys] for ys in xs]
        for xs in reversed(building)
    ]

    return buidling


def build(
    editor: Editor, building: List[List[List[Tuple[Structure, int]]]], place_air=True
):
    assert len(building[0]) in (1, 2), "Only buildings of height 1 or 2 are supported"

    # same for all strucures on ground floor
    gf_strucutre_size = ivec3(11, 5, 11)

    def build_layer(layer: int):
        for row_idx, building_row in tqdm(list(enumerate(reversed(building)))):
            with editor.pushTransform(
                Transform(
                    translation=ivec3(
                        row_idx * gf_strucutre_size.x, layer * gf_strucutre_size.y, 0
                    )
                )
            ):
                for col_idx, (structure, rotation) in enumerate(building_row[layer]):
                    with editor.pushTransform(
                        Transform(translation=ivec3(0, 0, col_idx * gf_strucutre_size.z))
                    ):
                        if not place_air and structure.name == "empty-space-air":
                            continue

                        build_structure(editor, structure, rotation)

                        if layer == 1 and structure.name != "school-upper-entrance":
                            with editor.pushTransform(Transform(translation=ivec3(0, 5, 0))):
                                structure_name = "school/school-roof"
                                with open("structures/" + structure_name + ".pkl", "rb") as f:
                                    structure = pickle.load(f)

                                # destination_pos = ivec3(-11, -60, 198)
                                print("Replicating building")
                                for vec, block in structure.blocks.items():
                                    # vec = (-vec[0], vec[1], vec[2]) # mirror at axis
                                    editor.placeBlock(vec, block)
                                editor.flushBuffer()

                    editor.flushBuffer()
                    time.sleep(0.1)

    build_layer(0)
    print("Ground floor finished")

    build_layer(1)
    print("Top floor finished")
    editor.flushBuffer()

    # build_layer(2)
    # print("Roof finished")
    # editor.flushBuffer()


def main():
    ED = Editor(buffering=True)

    try:
        ED.transform @= Transform(translation=ivec3(-623, -60, 199))

        print("Building house...")
        # building = deterministic_building()

        wfc = random_building(size=(7, 2, 7))
        building = wfc_state_to_minecraft_blocks(wfc.collapsed_state())
        build(editor=ED, building=building, place_air=False)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    check_symmetry(sa.structure_adjecencies)
    main()
