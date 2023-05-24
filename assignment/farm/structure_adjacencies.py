import logging

from assignment.farm.structures import (
    farm_outside_corner,
    farm_outside_corridor_corner,
    farm_outside_corridor_end,
    farm_outside_corridor_to_left,
    farm_outside_corridor_to_right,
    farm_outside_middle,
    farm_outside_wall,
    farm_corner,
    farm_corridor_straight,
    farm_corridor_to_farm,
    farm_corridor_to_left,
    farm_corridor_to_open,
    farm_corridor_to_right,
    farm_entrance,
    farm_middle,
    farm_wall,
    empty_space_air,
)
from assignment.utils.structure_adjacency import StructureAdjacency, all_rotations, check_symmetry
from assignment.utils.structure_rotation import StructureRotation

logger = logging.getLogger(__name__)


structure_adjecencies = {
    empty_space_air: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=empty_space_air,
        x_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(farm_outside_corridor_corner, 2),
            StructureRotation(farm_outside_corridor_corner, 3),
            StructureRotation(farm_outside_corner, 0),
            StructureRotation(farm_outside_corner, 1),
            StructureRotation(farm_outside_corridor_end, 0),
            StructureRotation(farm_outside_corridor_end, 1),
            StructureRotation(farm_outside_corridor_end, 2),
            StructureRotation(farm_outside_corridor_to_left, 2),
            StructureRotation(farm_outside_corridor_to_right, 0),
            StructureRotation(farm_outside_wall, 0),
            StructureRotation(farm_corner, 2),
            StructureRotation(farm_corner, 3),
            StructureRotation(farm_corridor_straight, 0),
            StructureRotation(farm_corridor_straight, 2),
            StructureRotation(farm_corridor_to_farm, 0),
            StructureRotation(farm_corridor_to_farm, 2),
            StructureRotation(farm_corridor_to_left, 2),
            StructureRotation(farm_corridor_to_right, 0),
            StructureRotation(farm_entrance, 1),
            StructureRotation(farm_entrance, 2),
            StructureRotation(farm_wall, 2),
        ],
        x_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(farm_outside_corridor_corner, 0),
            StructureRotation(farm_outside_corridor_corner, 1),
            StructureRotation(farm_outside_corner, 2),
            StructureRotation(farm_outside_corner, 3),
            StructureRotation(farm_outside_corridor_end, 0),
            StructureRotation(farm_outside_corridor_end, 2),
            StructureRotation(farm_outside_corridor_end, 3),
            StructureRotation(farm_outside_corridor_to_left, 0),
            StructureRotation(farm_outside_corridor_to_right, 2),
            StructureRotation(farm_outside_wall, 2),
            StructureRotation(farm_corner, 0),
            StructureRotation(farm_corner, 1),
            StructureRotation(farm_corridor_straight, 0),
            StructureRotation(farm_corridor_straight, 2),
            StructureRotation(farm_corridor_to_farm, 0),
            StructureRotation(farm_corridor_to_farm, 2),
            StructureRotation(farm_corridor_to_left, 0),
            StructureRotation(farm_corridor_to_right, 2),
            StructureRotation(farm_entrance, 0),
            StructureRotation(farm_entrance, 3),
            StructureRotation(farm_wall, 0),
        ],
        z_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(farm_outside_corridor_corner, 0),
            StructureRotation(farm_outside_corridor_corner, 3),
            StructureRotation(farm_outside_corner, 1),
            StructureRotation(farm_outside_corner, 2),
            StructureRotation(farm_outside_corridor_end, 1),
            StructureRotation(farm_outside_corridor_end, 2),
            StructureRotation(farm_outside_corridor_end, 3),
            StructureRotation(farm_outside_corridor_to_left, 3),
            StructureRotation(farm_outside_corridor_to_right, 1),
            StructureRotation(farm_outside_wall, 1),
            StructureRotation(farm_corner, 0),
            StructureRotation(farm_corner, 3),
            StructureRotation(farm_corridor_straight, 1),
            StructureRotation(farm_corridor_straight, 3),
            StructureRotation(farm_corridor_to_farm, 1),
            StructureRotation(farm_corridor_to_farm, 3),
            StructureRotation(farm_corridor_to_left, 3),
            StructureRotation(farm_corridor_to_right, 1),
            StructureRotation(farm_entrance, 2),
            StructureRotation(farm_entrance, 3),
            StructureRotation(farm_wall, 3),
        ],
        z_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(farm_outside_corridor_corner, 0),
            StructureRotation(farm_outside_corridor_corner, 3),
            StructureRotation(farm_outside_corner, 1),
            StructureRotation(farm_outside_corner, 2),
            StructureRotation(farm_outside_corridor_end, 0),
            StructureRotation(farm_outside_corridor_end, 1),
            StructureRotation(farm_outside_corridor_end, 3),
            StructureRotation(farm_outside_corridor_to_left, 1),
            StructureRotation(farm_outside_corridor_to_right, 3),
            StructureRotation(farm_outside_wall, 3),
            StructureRotation(farm_corner, 1),
            StructureRotation(farm_corner, 2),
            StructureRotation(farm_corridor_straight, 1),
            StructureRotation(farm_corridor_straight, 3),
            StructureRotation(farm_corridor_to_farm, 1),
            StructureRotation(farm_corridor_to_farm, 3),
            StructureRotation(farm_corridor_to_left, 1),
            StructureRotation(farm_corridor_to_right, 3),
            StructureRotation(farm_entrance, 0),
            StructureRotation(farm_entrance, 1),
            StructureRotation(farm_wall, 1),
        ],
    ),
    farm_outside_corridor_corner: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_outside_corridor_corner,
        x_plus=[
            *all_rotations(empty_space_air),
        ],
        x_minus=[
            StructureRotation(farm_outside_corridor_corner, 2),
            StructureRotation(farm_outside_corridor_corner, 3),
            StructureRotation(farm_outside_corridor_end, 1),
            StructureRotation(farm_outside_corridor_to_left, 3),
            StructureRotation(farm_outside_corridor_to_right, 3),
            StructureRotation(farm_corridor_to_farm, 3),
        ],
        z_plus=[
            StructureRotation(farm_outside_corridor_corner, 1),
            StructureRotation(farm_outside_corridor_corner, 2),
            StructureRotation(farm_outside_corridor_end, 0),
            StructureRotation(farm_outside_corridor_to_left, 2),
            StructureRotation(farm_outside_corridor_to_right, 2),
            StructureRotation(farm_corridor_to_farm, 2),
        ],
        z_minus=[
            *all_rotations(empty_space_air),
        ]
    ),
    farm_outside_corner: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_outside_corner,
        x_plus=[
            StructureRotation(farm_outside_corner, 3),
            StructureRotation(farm_outside_corridor_to_left, 0),
            StructureRotation(farm_outside_corridor_to_right, 3),
            StructureRotation(farm_outside_wall, 3),
        ],
        x_minus=[
            *all_rotations(empty_space_air),
        ],
        z_plus=[
            *all_rotations(empty_space_air),
        ],
        z_minus=[
            StructureRotation(farm_outside_corner, 1),
            StructureRotation(farm_outside_corridor_to_left, 2),
            StructureRotation(farm_corridor_to_right, 1),
            StructureRotation(farm_outside_wall, 0)
        ],
    ),
    farm_outside_corridor_end: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_outside_corridor_end,
        x_plus=[
            *all_rotations(empty_space_air),
        ],
        x_minus=[
            *all_rotations(empty_space_air),
        ],
        z_plus=[
            *all_rotations(empty_space_air),
        ],
        z_minus=[
            StructureRotation(farm_outside_corridor_corner, 0),
            StructureRotation(farm_outside_corridor_to_left, 0),
            StructureRotation(farm_outside_corridor_to_right, 0),
            StructureRotation(farm_corridor_to_farm, 0),
        ]
    ),
    farm_outside_corridor_to_left: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_outside_corridor_to_left,
        x_plus=[
            *all_rotations(empty_space_air),
        ],
        x_minus=[
            StructureRotation(farm_outside_corner,0),
            StructureRotation(farm_outside_corridor_to_left, 1),
            StructureRotation(farm_outside_corridor_to_right,0),
            StructureRotation(farm_outside_wall, 3),
        ],
        z_plus=[
            StructureRotation(farm_outside_corridor_corner, 1),
            StructureRotation(farm_outside_corridor_corner, 2),
            StructureRotation(farm_outside_corridor_end, 0),
            StructureRotation(farm_outside_corridor_to_left, 2),
            StructureRotation(farm_outside_corridor_to_right, 2),
            StructureRotation(farm_corridor_to_farm, 2),
        ],
        z_minus=[
            StructureRotation(farm_outside_corner, 2),
            StructureRotation(farm_outside_corridor_to_left, 3),
            StructureRotation(farm_outside_corridor_to_right, 2),
            StructureRotation(farm_outside_wall, 2)
        ]
    ),
    farm_outside_corridor_to_right: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_outside_corridor_to_right,
        x_plus=[
            StructureRotation(farm_outside_corner, 3),
            StructureRotation(farm_outside_corridor_to_left, 0),
            StructureRotation(farm_outside_corridor_to_right, 3),
            StructureRotation(farm_outside_wall, 3),
        ],
        x_minus=[
            *all_rotations(empty_space_air),
        ],
        z_plus=[
            StructureRotation(farm_outside_corridor_corner, 1),
            StructureRotation(farm_outside_corridor_corner, 2),
            StructureRotation(farm_outside_corridor_end, 0),
            StructureRotation(farm_outside_corridor_to_left, 2),
            StructureRotation(farm_outside_corridor_to_right, 2),
            StructureRotation(farm_corridor_to_farm, 2),
        ],
        z_minus=[
            StructureRotation(farm_outside_corner, 1),
            StructureRotation(farm_outside_corridor_to_left, 2),
            StructureRotation(farm_corridor_to_right, 1),
            StructureRotation(farm_outside_wall, 0)
        ],
    ),
    farm_outside_middle: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_outside_middle,
        x_plus=[
            StructureRotation(farm_outside_wall, 2),
        ],
        x_minus=[
            StructureRotation(farm_outside_wall, 0),
        ],
        z_plus=[
            StructureRotation(farm_outside_wall, 3),
        ],
        z_minus=[
            StructureRotation(farm_outside_wall, 1),
        ],
    ),
    farm_outside_wall: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_outside_wall,
        x_plus=[
            *all_rotations(farm_outside_middle),
        ],
        x_minus=[
            *all_rotations(empty_space_air),
        ],
        z_plus=[
            StructureRotation(farm_outside_wall, 0),
            StructureRotation(farm_outside_corner, 0),
            StructureRotation(farm_outside_corridor_to_left, 1),
            StructureRotation(farm_outside_corridor_to_right, 0),
        ],
        z_minus=[
            StructureRotation(farm_outside_wall, 0),
            StructureRotation(farm_outside_corner, 1),
            StructureRotation(farm_outside_corridor_to_left, 2),
            StructureRotation(farm_outside_corridor_to_right, 1),
        ]
    ),
    farm_corner: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_corner,
        x_plus=[
            *all_rotations(empty_space_air),
        ],
        x_minus=[
            StructureRotation(farm_corner, 3),
            StructureRotation(farm_corridor_to_left, 2),
            StructureRotation(farm_corridor_to_open, 2),
            StructureRotation(farm_corridor_to_right, 1),
            StructureRotation(farm_entrance, 2),
            StructureRotation(farm_wall, 3),
        ],
        z_plus=[
            StructureRotation(farm_corner, 1),
            StructureRotation(farm_corridor_to_left, 0),
            StructureRotation(farm_corridor_to_open, 3),
            StructureRotation(farm_corridor_to_right, 3),
            StructureRotation(farm_entrance, 0),
            StructureRotation(farm_wall, 0),
        ],
        z_minus=[
            *all_rotations(empty_space_air),
        ]
    ),
    farm_corridor_straight: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_corridor_straight,
        x_plus=[
            *all_rotations(empty_space_air),
        ],
        x_minus=[
            *all_rotations(empty_space_air),
        ],
        z_plus=[
            StructureRotation(farm_corridor_straight, 0),
            StructureRotation(farm_corridor_straight, 2),
            StructureRotation(farm_corridor_to_farm, 0),
            StructureRotation(farm_corridor_to_left, 2),
            StructureRotation(farm_corridor_to_open, 2),
            StructureRotation(farm_corridor_to_right, 2),
        ],
        z_minus=[
            StructureRotation(farm_corridor_straight, 0),
            StructureRotation(farm_corridor_straight, 2),
            StructureRotation(farm_corridor_to_farm, 2),
            StructureRotation(farm_corridor_to_left, 0),
            StructureRotation(farm_corridor_to_open, 0),
            StructureRotation(farm_corridor_to_right, 0),
        ]
    ),
    farm_corridor_to_farm: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_corridor_to_farm,
        x_plus=[
            *all_rotations(empty_space_air),
        ],
        x_minus=[
            *all_rotations(empty_space_air),
        ],
        z_plus=[
            StructureRotation(farm_outside_corridor_corner, 1),
            StructureRotation(farm_outside_corridor_corner, 2),
            StructureRotation(farm_outside_corridor_end, 2),
            StructureRotation(farm_outside_corridor_to_left, 0),
            StructureRotation(farm_outside_corridor_to_right, 0),
        ],
        z_minus=[
            StructureRotation(farm_corridor_straight, 0),
            StructureRotation(farm_corridor_straight, 2),
            StructureRotation(farm_corridor_to_left, 0),
            StructureRotation(farm_corridor_to_open, 0),
            StructureRotation(farm_corridor_to_right, 0),
        ],
    ),
    farm_corridor_to_left: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_corridor_to_left,
        x_plus=[
            *all_rotations(empty_space_air),
        ],
        x_minus=[
            StructureRotation(farm_corner, 2),
            StructureRotation(farm_corridor_to_left, 1),
            StructureRotation(farm_corridor_to_right, 0),
            StructureRotation(farm_corridor_to_open, 0),
            StructureRotation(farm_entrance, 1),
            StructureRotation(farm_wall, 1),
        ],
        z_plus=[
            StructureRotation(farm_corridor_straight, 0),
            StructureRotation(farm_corridor_straight, 2),
            StructureRotation(farm_corridor_to_farm, 0),
            StructureRotation(farm_corridor_to_left, 2),
            StructureRotation(farm_corridor_to_open, 2),
            StructureRotation(farm_corridor_to_right, 2),
        ],
        z_minus=[
            StructureRotation(farm_corner, 0),
            StructureRotation(farm_corridor_to_left, 3),
            StructureRotation(farm_corridor_to_right, 3),
            StructureRotation(farm_corridor_to_open, 2),
            StructureRotation(farm_entrance, 3),
            StructureRotation(farm_wall, 0),
        ]
    ),
    farm_corridor_to_open: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_corridor_to_open,
        x_plus=[
            StructureRotation(farm_corner, 1),
            StructureRotation(farm_corridor_to_left, 0),
            StructureRotation(farm_corridor_to_right, 3),
            StructureRotation(farm_corridor_to_open, 0),
            StructureRotation(farm_entrance, 0),
            StructureRotation(farm_wall, 1),
        ],
        x_minus=[
            StructureRotation(farm_corner, 2),
            StructureRotation(farm_corridor_to_left, 1),
            StructureRotation(farm_corridor_to_right, 0),
            StructureRotation(farm_corridor_to_open, 0),
            StructureRotation(farm_entrance, 1),
            StructureRotation(farm_wall, 1),
        ],
        z_plus=[
            StructureRotation(farm_corridor_straight, 0),
            StructureRotation(farm_corridor_straight, 2),
            StructureRotation(farm_corridor_to_farm, 0),
            StructureRotation(farm_corridor_to_left, 2),
            StructureRotation(farm_corridor_to_open, 2),
            StructureRotation(farm_corridor_to_right, 2),
        ],
        z_minus=[
            StructureRotation(farm_corridor_to_open, 2),
            *all_rotations(farm_middle),
            StructureRotation(farm_wall, 3),
        ]
    ),
    farm_corridor_to_right: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_corridor_to_right,
        x_plus=[
            StructureRotation(farm_corner, 1),
            StructureRotation(farm_corridor_to_left, 0),
            StructureRotation(farm_corridor_to_right, 3),
            StructureRotation(farm_corridor_to_open, 0),
            StructureRotation(farm_entrance, 0),
            StructureRotation(farm_wall, 1),
        ],
        x_minus=[
            *all_rotations(empty_space_air),
        ],
        z_plus=[
            StructureRotation(farm_corridor_straight, 0),
            StructureRotation(farm_corridor_straight, 2),
            StructureRotation(farm_corridor_to_farm, 0),
            StructureRotation(farm_corridor_to_left, 2),
            StructureRotation(farm_corridor_to_open, 2),
            StructureRotation(farm_corridor_to_right, 2),
        ],
        z_minus=[
            StructureRotation(farm_corner, 3),
            StructureRotation(farm_corridor_to_left, 2),
            StructureRotation(farm_corridor_to_right, 1),
            StructureRotation(farm_corridor_to_open, 1),
            StructureRotation(farm_entrance, 2),
            StructureRotation(farm_wall, 2),
        ],
    ),
    farm_entrance: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_entrance,
        x_plus=[
            *all_rotations(empty_space_air),
        ],
        x_minus=[
            StructureRotation(farm_corner, 2),
            StructureRotation(farm_corridor_to_left, 1),
            StructureRotation(farm_corridor_to_right, 0),
            StructureRotation(farm_corridor_to_open, 0),
            StructureRotation(farm_entrance, 1),
            StructureRotation(farm_wall, 1),
        ],
        z_plus=[
            *all_rotations(empty_space_air),
        ],
        z_minus=[
            StructureRotation(farm_corner, 0),
            StructureRotation(farm_corridor_to_left, 3),
            StructureRotation(farm_corridor_to_right, 3),
            StructureRotation(farm_corridor_to_open, 2),
            StructureRotation(farm_entrance, 3),
            StructureRotation(farm_wall, 0),
        ],
    ),
    farm_middle: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_middle,
        x_plus=[
            *all_rotations(farm_middle),
            StructureRotation(farm_corridor_to_open, 3),
            StructureRotation(farm_wall, 0),
        ],
        x_minus=[
            *all_rotations(farm_middle),
            StructureRotation(farm_corridor_to_open, 1),
            StructureRotation(farm_wall, 2),
        ],
        z_plus=[
            *all_rotations(farm_middle),
            StructureRotation(farm_corridor_to_open, 0),
            StructureRotation(farm_wall, 1),
        ],
        z_minus=[
            *all_rotations(farm_middle),
            StructureRotation(farm_corridor_to_open, 2),
            StructureRotation(farm_wall, 3),
        ]
    ),
    farm_wall: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=farm_wall,
        x_plus=[
            *all_rotations(empty_space_air),
        ],
        x_minus=[
            *all_rotations(farm_middle),
            StructureRotation(farm_corridor_to_open, 1),
            StructureRotation(farm_wall, 2),
        ],
        z_plus=[
            StructureRotation(farm_corner, 1),
            StructureRotation(farm_corridor_to_left, 0),
            StructureRotation(farm_corridor_to_open, 3),
            StructureRotation(farm_corridor_to_right, 3),
            StructureRotation(farm_entrance, 0),
            StructureRotation(farm_wall, 0),
        ],
        z_minus=[
            StructureRotation(farm_corner, 0),
            StructureRotation(farm_corridor_to_left, 3),
            StructureRotation(farm_corridor_to_right, 3),
            StructureRotation(farm_corridor_to_open, 2),
            StructureRotation(farm_entrance, 3),
            StructureRotation(farm_wall, 0),
        ],
    )
}