import time
from typing import List, Tuple

from gdpc import Editor, Transform
from glm import ivec3
from tqdm import tqdm

from assignment.bakery.structure_adjacency import (
    StructureRotation,
    all_rotations,
)

import assignment.bakery.structure_adjacency as sa

from assignment.bakery.structures import (
    bakery_corner_narrow_to_narrow,
    bakery_corner_narrow_to_wide,
    bakery_corner_wide_to_narrow,
    bakery_corner_wide_to_wide,
    bakery_corridor_corner,
    bakery_corridor_end,
    bakery_corridor_entrance,
    bakery_corridor_straight,
    bakery_corridor_to_left,
    bakery_corridor_to_open,
    bakery_corridor_to_right,
    bakery_entrance_open,
    bakery_inner_corner_narrow,
    bakery_inner_corner_wide,
    bakery_middle_chairs,
    bakery_middle_counter,
    bakery_oven_narrow,
    bakery_oven_wide,
    bakery_wall_counter,
    bakery_wall_narrow,
    bakery_wall_wide,
    empty_space_air,
)

from assignment.utils.structure import Structure, build_structure, load_structure
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
    size: Tuple[int, int, int] = (5, 1, 5), buildable: List[List[bool]] | None = None
) -> WaveFunctionCollapse:
    wfc = WaveFunctionCollapse(size, sa.structure_adjacencies, structure_weights)
    if buildable is None:
        buildable = [
            [True, True, True, True, True],
            [True, True, True, True, True],
            [False, False, False, True, True],
            [False, False, False, True, True],
            [False, False, False, True, True],
        ]

    def reinit():
        collapse_to_air_on_outer_rectangle(wfc)

        print("Outer rectangle")
        print_state(wfc)

        collapse_unbuildable_to_air(wfc, buildable)

        print("Unbuildable")
        print_state(wfc)

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
        any(
            [
                StructureRotation(bakery_entrance_open, r) in set(wfc.used_structures())
                for r in range(4)
            ]
        )
        # return (not air_only) and contains_door
        return True

    retries = wfc.collapse_with_retry(reinit=reinit)
    while not building_criterion_met(wfc):  # used air structures only
        wfc._initialize_state_space_superposition()
        retries += 1 + wfc.collapse_with_retry(reinit=reinit)
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


def build_bakery(
    editor: Editor, building: List[List[List[Tuple[Structure, int]]]], place_air=True
):
    assert len(building[0]) in (1, 2), "Only buildings of height 1 or 2 are supported"

    # same for all strucures on ground floor
    gf_strucutre_size = ivec3(7, 10, 7)

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
                        if not place_air and structure.name == empty_space_air:
                            continue

                        build_structure(editor, structure, rotation)
                    editor.flushBuffer()
                    time.sleep(0.1)

    build_layer(0)
    print("Ground floor finished")


def main():
    ED = Editor(buffering=True)

    try:
        ED.transform @= Transform(translation=ivec3(-100, 0, 200))

        print("Building house...")
        # building = deterministic_building()

        wfc = random_building()
        building = wfc_state_to_minecraft_blocks(wfc.collapsed_state())
        build_bakery(editor=ED, building=building, place_air=False)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
