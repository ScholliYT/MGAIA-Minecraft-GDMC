import logging

from generator.brickhouse.structures import (
    brickhouse_balcony,
    brickhouse_big_window_flat_roof,
    brickhouse_center,
    brickhouse_corner,
    brickhouse_courtyard,
    brickhouse_entrance,
    brickhouse_entrance_stairs,
    brickhouse_inner_corner_m2m,
    brickhouse_middle,
    brickhouse_roofhouse_center,
    brickhouse_roofhouse_corner,
    brickhouse_roofhouse_corner_stairs,
    brickhouse_roofhouse_courtyard,
    brickhouse_roofhouse_inner_corner_m2m,
    brickhouse_roofhouse_middle,
    brickhouse_roofhouse_middle_to_flat,
    brickhouse_roofhouse_middle_to_flat_mirrored_x,
    brickhouse_small_window_flat_roof,
    empty_space_air,
)
from generator.utils.structure_adjacency import StructureAdjacency, all_rotations, check_symmetry
from generator.utils.structure_rotation import StructureRotation

logger = logging.getLogger(__name__)


structure_adjecencies = {
    empty_space_air: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=empty_space_air,
        x_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(brickhouse_entrance, 1).rotate(
                3
            ),  # from brickhouse_entrance.x_minus
            StructureRotation(brickhouse_entrance, 1).rotate(
                2
            ),  # from brickhouse_entrance.z_minus
            StructureRotation(brickhouse_entrance_stairs, 1).rotate(
                3
            ),  # from brickhouse_entrance_stairs.x_minus
            StructureRotation(brickhouse_entrance_stairs, 1).rotate(
                2
            ),  # from brickhouse_entrance_stairs.z_minus
            StructureRotation(brickhouse_balcony, 1).rotate(3),  # from brickhouse_balcony.x_minus
            StructureRotation(brickhouse_balcony, 1).rotate(2),  # from brickhouse_balcony.z_minus
            StructureRotation(brickhouse_corner, 1).rotate(3),  # from brickhouse_corner.x_minus
            StructureRotation(brickhouse_corner, 1).rotate(2),  # from brickhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner, 1).rotate(
                3
            ),  # from brickhouse_roofhouse_corner.x_minus
            StructureRotation(brickhouse_roofhouse_corner, 1).rotate(
                2
            ),  # from brickhouse_roofhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner_stairs, 1).rotate(
                3
            ),  # from brickhouse_roofhouse_corner_stairs.x_minus
            StructureRotation(brickhouse_roofhouse_corner_stairs, 1).rotate(
                2
            ),  # from brickhouse_roofhouse_corner_stairs.z_minus
            StructureRotation(brickhouse_small_window_flat_roof, 1).rotate(
                3
            ),  # from brickhouse_small_window_flat_roof.x_minus
            StructureRotation(brickhouse_small_window_flat_roof, 1).rotate(
                2
            ),  # from brickhouse_small_window_flat_roof.z_minus
            StructureRotation(brickhouse_big_window_flat_roof, 1).rotate(
                3
            ),  # from brickhouse_big_window_flat_roof.x_minus
            StructureRotation(brickhouse_big_window_flat_roof, 1).rotate(
                2
            ),  # from brickhouse_big_window_flat_roof.z_minus
            StructureRotation(brickhouse_middle, 1).rotate(2),  # from brickhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle, 1).rotate(
                2
            ),  # from brickhouse_roofhouse_middle.z_minus
            StructureRotation(
                brickhouse_roofhouse_middle_to_flat, 0
            ),  # from brickhouse_roofhouse_middle_to_flat.x_minus
            StructureRotation(
                brickhouse_roofhouse_middle_to_flat_mirrored_x, 2
            ),  # from brickhouse_roofhouse_middle_to_flat_mirrored_x.x_plus
        ],
        x_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(brickhouse_entrance, 3).rotate(
                3
            ),  # from brickhouse_entrance.x_minus
            StructureRotation(brickhouse_entrance, 3).rotate(
                2
            ),  # from brickhouse_entrance.z_minus
            StructureRotation(brickhouse_entrance_stairs, 3).rotate(
                3
            ),  # from brickhouse_entrance_stairs.x_minus
            StructureRotation(brickhouse_entrance_stairs, 3).rotate(
                2
            ),  # from brickhouse_entrance_stairs.z_minus
            StructureRotation(brickhouse_balcony, 3).rotate(3),  # from brickhouse_balcony.x_minus
            StructureRotation(brickhouse_balcony, 3).rotate(2),  # from brickhouse_balcony.z_minus
            StructureRotation(brickhouse_corner, 3).rotate(3),  # from brickhouse_corner.x_minus
            StructureRotation(brickhouse_corner, 3).rotate(2),  # from brickhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner, 3).rotate(
                3
            ),  # from brickhouse_roofhouse_corner.x_minus
            StructureRotation(brickhouse_roofhouse_corner, 3).rotate(
                2
            ),  # from brickhouse_roofhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner_stairs, 3).rotate(
                3
            ),  # from brickhouse_roofhouse_corner_stairs.x_minus
            StructureRotation(brickhouse_roofhouse_corner_stairs, 3).rotate(
                2
            ),  # from brickhouse_roofhouse_corner_stairs.z_minus
            StructureRotation(brickhouse_small_window_flat_roof, 3).rotate(
                3
            ),  # from brickhouse_small_window_flat_roof.x_minus
            StructureRotation(brickhouse_small_window_flat_roof, 3).rotate(
                2
            ),  # from brickhouse_small_window_flat_roof.z_minus
            StructureRotation(brickhouse_big_window_flat_roof, 3).rotate(
                3
            ),  # from brickhouse_big_window_flat_roof.x_minus
            StructureRotation(brickhouse_big_window_flat_roof, 3).rotate(
                2
            ),  # from brickhouse_big_window_flat_roof.z_minus
            StructureRotation(brickhouse_middle, 3).rotate(2),  # from brickhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle, 3).rotate(
                2
            ),  # from brickhouse_roofhouse_middle.z_minus
            StructureRotation(
                brickhouse_roofhouse_middle_to_flat, 2
            ),  # from brickhouse_roofhouse_middle_to_flat.x_minus
            StructureRotation(
                brickhouse_roofhouse_middle_to_flat_mirrored_x, 0
            ),  # from brickhouse_roofhouse_middle_to_flat_mirrored_x.x_plus
        ],
        z_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(brickhouse_entrance, 2).rotate(
                3
            ),  # from brickhouse_entrance.x_minus
            StructureRotation(brickhouse_entrance, 2).rotate(
                2
            ),  # from brickhouse_entrance.z_minus
            StructureRotation(brickhouse_entrance_stairs, 2).rotate(
                3
            ),  # from brickhouse_entrance_stairs.x_minus
            StructureRotation(brickhouse_entrance_stairs, 2).rotate(
                2
            ),  # from brickhouse_entrance_stairs.z_minus
            StructureRotation(brickhouse_balcony, 2).rotate(3),  # from brickhouse_balcony.x_minus
            StructureRotation(brickhouse_balcony, 2).rotate(2),  # from brickhouse_balcony.z_minus
            StructureRotation(brickhouse_corner, 2).rotate(3),  # from brickhouse_corner.x_minus
            StructureRotation(brickhouse_corner, 2).rotate(2),  # from brickhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner, 2).rotate(
                3
            ),  # from brickhouse_roofhouse_corner.x_minus
            StructureRotation(brickhouse_roofhouse_corner, 2).rotate(
                2
            ),  # from brickhouse_roofhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner_stairs, 2).rotate(
                3
            ),  # from brickhouse_roofhouse_corner_stairs.x_minus
            StructureRotation(brickhouse_roofhouse_corner_stairs, 2).rotate(
                2
            ),  # from brickhouse_roofhouse_corner_stairs.z_minus
            StructureRotation(brickhouse_small_window_flat_roof, 2).rotate(
                3
            ),  # from brickhouse_small_window_flat_roof.x_minus
            StructureRotation(brickhouse_small_window_flat_roof, 2).rotate(
                2
            ),  # from brickhouse_small_window_flat_roof.z_minus
            StructureRotation(brickhouse_big_window_flat_roof, 2).rotate(
                3
            ),  # from brickhouse_big_window_flat_roof.x_minus
            StructureRotation(brickhouse_big_window_flat_roof, 2).rotate(
                2
            ),  # from brickhouse_big_window_flat_roof.z_minus
            StructureRotation(brickhouse_middle, 2).rotate(2),  # from brickhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle, 2).rotate(
                2
            ),  # from brickhouse_roofhouse_middle.z_minus
            StructureRotation(
                brickhouse_roofhouse_middle_to_flat, 1
            ),  # from brickhouse_roofhouse_middle_to_flat.x_minus
            StructureRotation(
                brickhouse_roofhouse_middle_to_flat_mirrored_x, 3
            ),  # from brickhouse_roofhouse_middle_to_flat_mirrored_x.x_plus
        ],
        z_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(brickhouse_entrance, 0).rotate(
                3
            ),  # from brickhouse_entrance.x_minus
            StructureRotation(brickhouse_entrance, 0).rotate(
                2
            ),  # from brickhouse_entrance.z_minus
            StructureRotation(brickhouse_entrance_stairs, 0).rotate(
                3
            ),  # from brickhouse_entrance_stairs.x_minus
            StructureRotation(brickhouse_entrance_stairs, 0).rotate(
                2
            ),  # from brickhouse_entrance_stairs.z_minus
            StructureRotation(brickhouse_balcony, 0).rotate(3),  # from brickhouse_balcony.x_minus
            StructureRotation(brickhouse_balcony, 0).rotate(2),  # from brickhouse_balcony.z_minus
            StructureRotation(brickhouse_corner, 0).rotate(3),  # from brickhouse_corner.x_minus
            StructureRotation(brickhouse_corner, 0).rotate(2),  # from brickhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner, 0).rotate(
                3
            ),  # from brickhouse_roofhouse_corner.x_minus
            StructureRotation(brickhouse_roofhouse_corner, 0).rotate(
                2
            ),  # from brickhouse_roofhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner_stairs, 0).rotate(
                3
            ),  # from brickhouse_roofhouse_corner_stairs.x_minus
            StructureRotation(brickhouse_roofhouse_corner_stairs, 0).rotate(
                2
            ),  # from brickhouse_roofhouse_corner_stairs.z_minus
            StructureRotation(brickhouse_small_window_flat_roof, 0).rotate(
                3
            ),  # from brickhouse_small_window_flat_roof.x_minus
            StructureRotation(brickhouse_small_window_flat_roof, 0).rotate(
                2
            ),  # from brickhouse_small_window_flat_roof.z_minus
            StructureRotation(brickhouse_big_window_flat_roof, 0).rotate(
                3
            ),  # from brickhouse_big_window_flat_roof.x_minus
            StructureRotation(brickhouse_big_window_flat_roof, 0).rotate(
                2
            ),  # from brickhouse_big_window_flat_roof.z_minus
            StructureRotation(brickhouse_middle, 0).rotate(2),  # from brickhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle, 0).rotate(
                2
            ),  # from brickhouse_roofhouse_middle.z_minus
            StructureRotation(
                brickhouse_roofhouse_middle_to_flat, 3
            ),  # from brickhouse_roofhouse_middle_to_flat.x_minus
            StructureRotation(
                brickhouse_roofhouse_middle_to_flat_mirrored_x, 1
            ),  # from brickhouse_roofhouse_middle_to_flat_mirrored_x.x_plus
        ],
        y_plus=[*all_rotations(empty_space_air)],
        y_minus=[*all_rotations(empty_space_air)],
    ),
    brickhouse_entrance: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_entrance,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
            StructureRotation(brickhouse_entrance_stairs, 1),
            StructureRotation(brickhouse_balcony, 1),
            StructureRotation(brickhouse_corner, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 3),
            StructureRotation(brickhouse_entrance, 3),
            StructureRotation(brickhouse_entrance_stairs, 3),
            StructureRotation(brickhouse_balcony, 3),
            StructureRotation(brickhouse_corner, 3),
        ],
        y_plus=[
            StructureRotation(brickhouse_small_window_flat_roof, 0),
            StructureRotation(brickhouse_roofhouse_corner, 0),
        ],
    ),
    brickhouse_entrance_stairs: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_entrance_stairs,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
            StructureRotation(brickhouse_entrance_stairs, 1),
            StructureRotation(brickhouse_balcony, 1),
            StructureRotation(brickhouse_corner, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 3),
            StructureRotation(brickhouse_entrance, 3),
            StructureRotation(brickhouse_entrance_stairs, 3),
            StructureRotation(brickhouse_balcony, 3),
            StructureRotation(brickhouse_corner, 3),
        ],
        y_plus=[
            StructureRotation(brickhouse_roofhouse_corner_stairs, 0),
        ],
    ),
    brickhouse_balcony: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_balcony,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
            StructureRotation(brickhouse_entrance_stairs, 1),
            StructureRotation(brickhouse_balcony, 1),
            StructureRotation(brickhouse_corner, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 3),
            StructureRotation(brickhouse_entrance, 3),
            StructureRotation(brickhouse_entrance_stairs, 3),
            StructureRotation(brickhouse_balcony, 3),
            StructureRotation(brickhouse_corner, 3),
        ],
        y_plus=[
            StructureRotation(brickhouse_small_window_flat_roof, 0),
            StructureRotation(brickhouse_roofhouse_corner, 0),
        ],
    ),
    brickhouse_corner: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_corner,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
            StructureRotation(brickhouse_entrance_stairs, 1),
            StructureRotation(brickhouse_balcony, 1),
            StructureRotation(brickhouse_corner, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 3),
            StructureRotation(brickhouse_entrance, 3),
            StructureRotation(brickhouse_entrance_stairs, 3),
            StructureRotation(brickhouse_balcony, 3),
            StructureRotation(brickhouse_corner, 3),
        ],
        y_plus=[
            StructureRotation(brickhouse_big_window_flat_roof, 0),
        ],
    ),
    brickhouse_middle: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_middle,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
            StructureRotation(brickhouse_entrance_stairs, 1),
            StructureRotation(brickhouse_balcony, 1),
            StructureRotation(brickhouse_corner, 1),
            StructureRotation(brickhouse_inner_corner_m2m, 1),
        ],
        x_minus=[
            StructureRotation(brickhouse_entrance, 0),
            StructureRotation(brickhouse_entrance_stairs, 0),
            StructureRotation(brickhouse_balcony, 0),
            StructureRotation(brickhouse_corner, 0),
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_inner_corner_m2m, 2),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 2),
            *all_rotations(brickhouse_center),
            *all_rotations(brickhouse_courtyard),
            StructureRotation(brickhouse_inner_corner_m2m, 0),
            StructureRotation(brickhouse_inner_corner_m2m, 3),
        ],
        y_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 0),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 1),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 3),
        ],
    ),
    brickhouse_center: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_center,
        x_plus=[
            *all_rotations(brickhouse_center),
            *all_rotations(brickhouse_courtyard),
            StructureRotation(brickhouse_middle, 1),
            StructureRotation(brickhouse_inner_corner_m2m, 3),
            StructureRotation(brickhouse_inner_corner_m2m, 2),
        ],
        x_minus=[
            *all_rotations(brickhouse_center),
            *all_rotations(brickhouse_courtyard),
            StructureRotation(brickhouse_middle, 3),
            StructureRotation(brickhouse_inner_corner_m2m, 1),
            StructureRotation(brickhouse_inner_corner_m2m, 0),
        ],
        z_plus=[
            *all_rotations(brickhouse_center),
            *all_rotations(brickhouse_courtyard),
            StructureRotation(brickhouse_middle, 2),
            StructureRotation(brickhouse_inner_corner_m2m, 0),
            StructureRotation(brickhouse_inner_corner_m2m, 3),
        ],
        z_minus=[
            *all_rotations(brickhouse_center),
            *all_rotations(brickhouse_courtyard),
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_inner_corner_m2m, 2),
            StructureRotation(brickhouse_inner_corner_m2m, 1),
        ],
        y_plus=[*all_rotations(brickhouse_roofhouse_center)],
    ),
    brickhouse_courtyard: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_courtyard,
        x_plus=[
            StructureRotation(brickhouse_middle, 1),
            *all_rotations(brickhouse_center),
        ],
        x_minus=[
            StructureRotation(brickhouse_middle, 3),
            *all_rotations(brickhouse_center),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 2),
            *all_rotations(brickhouse_center),
        ],
        z_minus=[
            StructureRotation(brickhouse_middle, 0),
            *all_rotations(brickhouse_center),
        ],
        y_plus=[*all_rotations(brickhouse_roofhouse_courtyard)],
    ),
    brickhouse_inner_corner_m2m: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_inner_corner_m2m,
        x_plus=[
            StructureRotation(brickhouse_middle, 1),
            *all_rotations(brickhouse_center),
        ],
        x_minus=[
            StructureRotation(brickhouse_middle, 2),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 3),
        ],
        z_minus=[
            StructureRotation(brickhouse_middle, 0),
            *all_rotations(brickhouse_center),
        ],
        y_plus=[
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 0),
        ],
    ),
    brickhouse_roofhouse_corner: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_roofhouse_corner,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 1),
            StructureRotation(brickhouse_roofhouse_corner_stairs, 1),
            StructureRotation(brickhouse_roofhouse_middle, 0),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 3),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 3),
            StructureRotation(brickhouse_roofhouse_corner_stairs, 3),
            StructureRotation(brickhouse_roofhouse_middle, 3),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 0),
        ],
        y_minus=[
            StructureRotation(brickhouse_entrance, 0),
            StructureRotation(brickhouse_balcony, 0),
        ],
    ),
    brickhouse_roofhouse_corner_stairs: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_roofhouse_corner_stairs,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 1),
            StructureRotation(brickhouse_roofhouse_corner_stairs, 1),
            StructureRotation(brickhouse_roofhouse_middle, 0),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 3),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 3),
            StructureRotation(brickhouse_roofhouse_corner_stairs, 3),
            StructureRotation(brickhouse_roofhouse_middle, 3),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 0),
        ],
        y_minus=[
            StructureRotation(brickhouse_entrance_stairs, 0),
        ],
    ),
    brickhouse_roofhouse_inner_corner_m2m: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_roofhouse_inner_corner_m2m,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 1),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        x_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 2),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 3),
        ],
        z_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 0),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        y_minus=[
            StructureRotation(brickhouse_inner_corner_m2m, 0),
        ],
    ),
    brickhouse_small_window_flat_roof: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_small_window_flat_roof,
        x_plus=[
            StructureRotation(brickhouse_big_window_flat_roof, 1),
            StructureRotation(brickhouse_small_window_flat_roof, 1),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_big_window_flat_roof, 3),
            StructureRotation(brickhouse_small_window_flat_roof, 3),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 2),
        ],
        y_minus=[
            StructureRotation(brickhouse_entrance, 0),
            StructureRotation(brickhouse_balcony, 0),
        ],
    ),
    brickhouse_big_window_flat_roof: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_big_window_flat_roof,
        x_plus=[
            StructureRotation(brickhouse_big_window_flat_roof, 1),
            StructureRotation(brickhouse_small_window_flat_roof, 1),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_big_window_flat_roof, 3),
            StructureRotation(brickhouse_small_window_flat_roof, 3),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 2),
        ],
        y_minus=[
            StructureRotation(brickhouse_corner, 0),
        ],
    ),
    brickhouse_roofhouse_middle: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_roofhouse_middle,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 1),
            StructureRotation(brickhouse_roofhouse_corner_stairs, 1),
            StructureRotation(brickhouse_roofhouse_middle, 0),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 1),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 3),
        ],
        x_minus=[
            StructureRotation(brickhouse_roofhouse_corner, 0),
            StructureRotation(brickhouse_roofhouse_corner_stairs, 0),
            StructureRotation(brickhouse_roofhouse_middle, 0),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 2),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 2),
            *all_rotations(brickhouse_roofhouse_courtyard),
            *all_rotations(brickhouse_roofhouse_center),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 0),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 3),
        ],
        y_minus=[
            StructureRotation(brickhouse_middle, 0),
        ],
    ),
    brickhouse_roofhouse_courtyard: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_roofhouse_courtyard,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 1),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        x_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 3),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 2),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        z_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 0),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        y_minus=[*all_rotations(brickhouse_courtyard)],
    ),
    brickhouse_roofhouse_center: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_roofhouse_center,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 1),
            *all_rotations(brickhouse_roofhouse_courtyard),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 3),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 2),
        ],
        x_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 3),
            *all_rotations(brickhouse_roofhouse_courtyard),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 1),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 0),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 2),
            *all_rotations(brickhouse_roofhouse_courtyard),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 0),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 3),
        ],
        z_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 0),
            *all_rotations(brickhouse_roofhouse_courtyard),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 2),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 1),
        ],
        y_minus=[*all_rotations(brickhouse_center)],
    ),
    brickhouse_roofhouse_middle_to_flat: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_roofhouse_middle_to_flat,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 0),
        ],
        z_plus=[
            StructureRotation(brickhouse_small_window_flat_roof, 3),
            StructureRotation(brickhouse_big_window_flat_roof, 3),
        ],
        z_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 3),
            StructureRotation(brickhouse_roofhouse_corner, 0),
            StructureRotation(brickhouse_roofhouse_corner_stairs, 0),
        ],
        y_minus=[
            StructureRotation(brickhouse_middle, 3),
        ],
    ),
    brickhouse_roofhouse_middle_to_flat_mirrored_x: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=brickhouse_roofhouse_middle_to_flat_mirrored_x,
        x_minus=[
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 0),
        ],
        z_plus=[
            StructureRotation(brickhouse_small_window_flat_roof, 2),
            StructureRotation(brickhouse_big_window_flat_roof, 2),
        ],
        z_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 1),
            StructureRotation(brickhouse_roofhouse_corner, 1),
            StructureRotation(brickhouse_roofhouse_corner_stairs, 1),
        ],
        y_minus=[
            StructureRotation(brickhouse_middle, 1),
        ],
    ),
}

if __name__ == "__main__":
    print(structure_adjecencies[brickhouse_entrance].adjecent_structrues("z_minus", 3))

    check_symmetry(structure_adjecencies)
