import time
from typing import List, Tuple

from gdpc import Editor, Transform
from glm import ivec3
from tqdm import tqdm

from assignment.brickhouse.structure_adjacencies import (
    structure_adjecencies,
)
from assignment.brickhouse.structures import (
    brickhouse_balcony,
    brickhouse_big_window_flat_roof,
    brickhouse_center,
    brickhouse_corner,
    brickhouse_courtyard,
    brickhouse_entrance,
    brickhouse_inner_corner_m2m,
    brickhouse_middle,
    brickhouse_roofhouse_center,
    brickhouse_roofhouse_corner,
    brickhouse_roofhouse_courtyard,
    brickhouse_roofhouse_inner_corner_m2m,
    brickhouse_roofhouse_middle,
    brickhouse_roofhouse_middle_to_flat,
    brickhouse_small_window_flat_roof,
    empty_space_air,
)
from assignment.utils.not_collapsable_exception import NotCollapsableException
from assignment.utils.structure import Structure, build_structure, load_structure
from assignment.utils.structure_adjacency import all_rotations
from assignment.utils.structure_rotation import StructureRotation
from assignment.utils.wave_function_collaplse_util import (
    collapse_to_air_on_outer_rectangle,
    collapse_unbuildable_to_air,
    print_state,
)
from assignment.utils.wave_function_collapse import WaveFunctionCollapse


def deterministic_building() -> List[List[List[Tuple[Structure, int]]]]:
    load_structure(brickhouse_entrance)
    middle_structure = load_structure(brickhouse_middle)
    load_structure(brickhouse_balcony)
    load_structure(brickhouse_corner)
    load_structure(brickhouse_center)
    load_structure(brickhouse_courtyard)
    load_structure(brickhouse_small_window_flat_roof)
    load_structure(brickhouse_big_window_flat_roof)
    load_structure(brickhouse_roofhouse_corner)
    roofhouse_middle_structure = load_structure(brickhouse_roofhouse_middle)
    load_structure(brickhouse_roofhouse_courtyard)
    load_structure(brickhouse_roofhouse_center)
    inner_corner_m2m_structure = load_structure(brickhouse_inner_corner_m2m)
    roofhouse_inner_corner_m2m_structure = load_structure(brickhouse_roofhouse_inner_corner_m2m)
    empty_space_air_structure = load_structure(empty_space_air)

    # building: List[List[Tuple[Structure, int]]] = [
    #     [(entrance_structure, 1), (entrance_structure, 2)],
    #     [(middle_structure, 0), (middle_structure, 2)],
    #     [(middle_structure, 0), (middle_structure, 2)],
    #     [(entrance_structure, 0), (entrance_structure, 3)],
    # ]

    # building: List[List[Tuple[Structure, int]]] = [
    #     [(entrance_structure, 1), (middle_structure, 1), (entrance_structure, 2)],
    #     [(entrance_structure, 0), (middle_structure, 3), (entrance_structure, 3)],
    # ]

    # building: List[List[Tuple[Structure, int]]] = [
    #     [(entrance_structure, 1), (middle_structure, 1), (balcony_structure, 2)],
    #     [(entrance_structure, 0), (middle_structure, 3), (corner_structure, 3)],
    # ]

    # 3x1x2 ground floor
    # building: List[List[Tuple[Structure, int]]] = [
    #     [(entrance_structure, 1), (middle_structure, 1), (entrance_structure, 2)],
    #     [(middle_structure, 0), (courtyard_structure, 0),  (middle_structure, 2)],
    #     [(entrance_structure, 0), (middle_structure, 3), (entrance_structure, 3)],
    # ]

    # 3x1x2 roof
    # building: List[List[List[Tuple[Structure, int]]]] = \
    # [
    #     [[(roofhouse_corner_structure, 1), (roofhouse_middle_structure, 1), (roofhouse_corner_structure, 2)]],
    #     [[(roofhouse_middle_structure, 0), (roofhouse_courtyard_structure, 0),  (roofhouse_middle_structure, 2)]],
    #     [[(roofhouse_corner_structure, 0), (roofhouse_middle_structure, 3), (roofhouse_corner_structure, 3)]],
    # ]

    # inner corner roof test
    # building: List[List[List[Tuple[Structure, int]]]] = \
    # [
    #     [
    #         [(roofhouse_inner_corner_m2m_structure, 0), (roofhouse_middle_structure, 3)]
    #     ],
    #     [
    #         [(roofhouse_middle_structure, 2), (empty_space_air_structure, 0)]
    #     ],
    # ]

    # inner corner test
    building: List[List[List[Tuple[Structure, int]]]] = [
        [
            [(inner_corner_m2m_structure, 0), (middle_structure, 3)],
            [(roofhouse_inner_corner_m2m_structure, 0), (roofhouse_middle_structure, 3)],
        ],
        [
            [(middle_structure, 2), (empty_space_air_structure, 0)],
            [(roofhouse_middle_structure, 2), (empty_space_air_structure, 0)],
        ],
    ]

    return building


def structure_weights(structures: List[StructureRotation]):
    for s in structures:
        if s.structure_name == empty_space_air:
            yield 0.001
        elif s.structure_name in (
            brickhouse_roofhouse_courtyard,
            brickhouse_center,
            brickhouse_inner_corner_m2m,
        ):
            yield 300.0
        elif s.structure_name in (brickhouse_roofhouse_middle_to_flat):
            yield 5.0
        else:
            yield 1.0


def random_building(
    size: Tuple[int, int, int] = (5, 2, 5),
    buildable: List[List[bool]] | None = None,
    max_retries=50,
) -> WaveFunctionCollapse:
    wfc = WaveFunctionCollapse(size, structure_adjecencies, structure_weights)
    if buildable is None:
        buildable = [
            [True, True, True, True, True],
            [True, True, True, True, True],
            [False, False, False, True, True],
            [False, False, False, True, True],
            [False, False, False, True, True],
        ]

    def reinit():
        collapse_to_air_on_outer_rectangle(wfc, empty_space_air)

        print("Removing outer rectangle from WFC state")
        print_state(wfc, air_name=empty_space_air)

        collapse_unbuildable_to_air(wfc, buildable, empty_space_air)

        print("Removing unbuildable area from WFC state")
        print_state(wfc, air_name=empty_space_air)

        # wfc.collapse_random_cell()
        wfc.collapse_random_cell()
        wfc.collapse_random_cell()
        wfc.collapse_random_cell()
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
        air_only = set(wfc.used_structures()).issubset(set([*all_rotations(empty_space_air)]))
        contains_door = any(
            [
                StructureRotation(brickhouse_entrance, r) in set(wfc.used_structures())
                for r in range(4)
            ]
        )
        return (not air_only) and contains_door

    retries = wfc.collapse_with_retry(reinit=reinit)
    while not building_criterion_met(wfc) and retries < max_retries:  # used air structures only
        wfc._initialize_state_space_superposition()
        retries += 1 + wfc.collapse_with_retry(reinit=reinit)

    if retries >= max_retries:
        raise NotCollapsableException()
    print(f"WFC collapsed after {retries} retries")
    print_state(wfc, air_name=empty_space_air)
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


def build(editor: Editor, building: List[List[List[Tuple[Structure, int]]]], place_air=True):
    assert len(building[0]) in (1, 2), "Only buildings of height 1 or 2 are supported"

    # same for all strucures on ground floor
    gf_structure_size = ivec3(11, 7, 11)

    def build_layer(layer: int):
        for row_idx, building_row in tqdm(list(enumerate(reversed(building)))):
            with editor.pushTransform(
                Transform(
                    translation=ivec3(
                        row_idx * gf_structure_size.x, layer * gf_structure_size.y, 0
                    )
                )
            ):
                for col_idx, (structure, rotation) in enumerate(building_row[layer]):
                    with editor.pushTransform(
                        Transform(translation=ivec3(0, 0, col_idx * gf_structure_size.z))
                    ):
                        if not place_air and structure.name == empty_space_air:
                            continue

                        build_structure(editor, structure, rotation)
                    editor.flushBuffer()
                    time.sleep(0.1)

    build_layer(0)
    print("Ground floor finished")

    build_layer(1)
    print("Top floor finished")
    editor.flushBuffer()


def main():
    ED = Editor(buffering=True)

    try:
        ED.transform @= Transform(translation=ivec3(-100, 0, 200))

        print("Building house...")
        # building = deterministic_building()

        wfc = random_building(size=(7, 2, 7))
        building = wfc_state_to_minecraft_blocks(wfc.collapsed_state())
        build(editor=ED, building=building, place_air=False)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
