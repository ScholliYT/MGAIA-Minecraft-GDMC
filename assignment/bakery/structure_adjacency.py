import logging
from dataclasses import dataclass, field, replace
from typing import Dict, List

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

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StructureRotation:
    structure_name: str
    rotation: int

    def rotate(self, amount: int):
        return replace(self, rotation=(self.rotation + amount) % 4)


@dataclass(frozen=True)
class StructureAdjacency:
    """Store all possible other Structures that can be placed next to this structure

    Assumes that this structure is rotated by 0
    """

    structure_name: str

    # store a list of structures that can be adjacent in the specified rotation and placed above this
    # (strucutre_name, rotation)
    y_plus: List[StructureRotation] = field(default_factory=list)
    y_minus: List[StructureRotation] = field(default_factory=list)

    x_plus: List[StructureRotation] = field(default_factory=lambda: all_rotations(empty_space_air))
    x_minus: List[StructureRotation] = field(
        default_factory=lambda: all_rotations(empty_space_air)
    )

    z_plus: List[StructureRotation] = field(default_factory=lambda: all_rotations(empty_space_air))
    z_minus: List[StructureRotation] = field(
        default_factory=lambda: all_rotations(empty_space_air)
    )

    def adjecent_structures(self, axis: str, self_rotation: int) -> List[StructureRotation]:
        if axis not in ("y_plus", "y_minus", "x_plus", "x_minus", "z_plus", "z_minus"):
            raise ValueError("Invalid axis " + axis)

        # easy cases since everything will rotate along the y-axis
        match axis:
            case "y_plus":
                return list(map(lambda r: r.rotate(self_rotation), self.y_plus))
            case "y_minus":
                return list(map(lambda r: r.rotate(self_rotation), self.y_minus))

        if self_rotation == 0:
            # default case with no rotations
            return getattr(self, axis)
        elif self_rotation in (1, 2, 3):
            rotation_axes = (self.x_plus, self.z_plus, self.x_minus, self.z_minus)
            match axis:
                case "x_plus":
                    return list(
                        map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 0])
                    )  # self.z_minus for rotation 1
                case "z_plus":
                    return list(
                        map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 1])
                    )  # self.x_plus for rotation 1
                case "x_minus":
                    return list(
                        map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 2])
                    )  # self.z_plus for rotation 1
                case "z_minus":
                    return list(
                        map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 3])
                    )  # self.x_minus for rotation 1
            raise NotImplementedError(f"Axis {axis} should have been handled before")
        else:
            raise ValueError("Rotation must be 0,1,2 or 3")


def all_rotations(structure: str):
    return [StructureRotation(structure, r) for r in range(4)]


structure_adjacencies = {
    empty_space_air: StructureAdjacency(
        structure_name=empty_space_air,
        x_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(bakery_corner_narrow_to_narrow, 1),
            StructureRotation(bakery_corner_narrow_to_narrow, 2),
            StructureRotation(bakery_corner_narrow_to_wide, 1),
            StructureRotation(bakery_corner_narrow_to_wide, 2),
            StructureRotation(bakery_corner_wide_to_narrow, 0),
            StructureRotation(bakery_corner_wide_to_narrow, 1),
            StructureRotation(bakery_corner_wide_to_wide, 0),
            StructureRotation(bakery_corner_wide_to_wide, 3),
            StructureRotation(bakery_corridor_corner, 2),
            StructureRotation(bakery_corridor_corner, 3),
            StructureRotation(bakery_corridor_end, 0),
            StructureRotation(bakery_corridor_end, 1),
            StructureRotation(bakery_corridor_end, 2),
            StructureRotation(bakery_corridor_entrance, 0),
            StructureRotation(bakery_corridor_entrance, 1),
            StructureRotation(bakery_corridor_entrance, 2),
            StructureRotation(bakery_corridor_straight, 0),
            StructureRotation(bakery_corridor_straight, 2),
            StructureRotation(bakery_corridor_to_left, 2),
            StructureRotation(bakery_corridor_to_right, 0),
            StructureRotation(bakery_entrance_open, 1),
            StructureRotation(bakery_oven_narrow, 2),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_counter, 1),
            StructureRotation(bakery_wall_narrow, 2),
            StructureRotation(bakery_wall_wide, 2),
        ],
        x_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(bakery_corner_narrow_to_narrow, 0),
            StructureRotation(bakery_corner_narrow_to_narrow, 3),
            StructureRotation(bakery_corner_narrow_to_wide, 0),
            StructureRotation(bakery_corner_narrow_to_wide, 3),
            StructureRotation(bakery_corner_wide_to_narrow, 2),
            StructureRotation(bakery_corner_wide_to_narrow, 3),
            StructureRotation(bakery_corner_wide_to_wide, 1),
            StructureRotation(bakery_corner_wide_to_wide, 2),
            StructureRotation(bakery_corridor_corner, 0),
            StructureRotation(bakery_corridor_corner, 1),
            StructureRotation(bakery_corridor_end, 0),
            StructureRotation(bakery_corridor_end, 2),
            StructureRotation(bakery_corridor_end, 3),
            StructureRotation(bakery_corridor_entrance, 0),
            StructureRotation(bakery_corridor_entrance, 2),
            StructureRotation(bakery_corridor_entrance, 3),
            StructureRotation(bakery_corridor_straight, 0),
            StructureRotation(bakery_corridor_straight, 2),
            StructureRotation(bakery_corridor_to_left, 0),
            StructureRotation(bakery_corridor_to_right, 2),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_oven_narrow, 0),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_counter, 3),
            StructureRotation(bakery_wall_narrow, 0),
            StructureRotation(bakery_wall_wide, 0),
        ],
        z_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(bakery_corner_narrow_to_narrow, 0),
            StructureRotation(bakery_corner_narrow_to_narrow, 1),
            StructureRotation(bakery_corner_narrow_to_wide, 0),
            StructureRotation(bakery_corner_narrow_to_wide, 1),
            StructureRotation(bakery_corner_wide_to_narrow, 0),
            StructureRotation(bakery_corner_wide_to_narrow, 3),
            StructureRotation(bakery_corner_wide_to_wide, 2),
            StructureRotation(bakery_corner_wide_to_wide, 3),
            StructureRotation(bakery_corridor_corner, 1),
            StructureRotation(bakery_corridor_corner, 2),
            StructureRotation(bakery_corridor_end, 0),
            StructureRotation(bakery_corridor_end, 1),
            StructureRotation(bakery_corridor_end, 3),
            StructureRotation(bakery_corridor_entrance, 0),
            StructureRotation(bakery_corridor_entrance, 1),
            StructureRotation(bakery_corridor_entrance, 3),
            StructureRotation(bakery_corridor_straight, 1),
            StructureRotation(bakery_corridor_straight, 3),
            StructureRotation(bakery_corridor_to_left, 1),
            StructureRotation(bakery_corridor_to_right, 3),
            StructureRotation(bakery_entrance_open, 0),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_oven_wide, 1),
            StructureRotation(bakery_wall_counter, 0),
            StructureRotation(bakery_wall_narrow, 1),
            StructureRotation(bakery_wall_wide, 1),            
        ],
        z_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(bakery_corner_narrow_to_narrow, 2),
            StructureRotation(bakery_corner_narrow_to_narrow, 3),
            StructureRotation(bakery_corner_narrow_to_wide, 2),
            StructureRotation(bakery_corner_narrow_to_wide, 3),
            StructureRotation(bakery_corner_wide_to_narrow, 1),
            StructureRotation(bakery_corner_wide_to_narrow, 2),
            StructureRotation(bakery_corner_wide_to_wide, 0),
            StructureRotation(bakery_corner_wide_to_wide, 1),
            StructureRotation(bakery_corridor_corner, 0),
            StructureRotation(bakery_corridor_corner, 3),
            StructureRotation(bakery_corridor_end, 1),
            StructureRotation(bakery_corridor_end, 2),
            StructureRotation(bakery_corridor_end, 3),
            StructureRotation(bakery_corridor_entrance, 1),
            StructureRotation(bakery_corridor_entrance, 2),
            StructureRotation(bakery_corridor_entrance, 3),
            StructureRotation(bakery_corridor_straight, 1),
            StructureRotation(bakery_corridor_straight, 3),
            StructureRotation(bakery_corridor_to_left, 3),
            StructureRotation(bakery_corridor_to_right, 1),
            StructureRotation(bakery_entrance_open, 2),
            StructureRotation(bakery_oven_narrow, 3),
            StructureRotation(bakery_oven_wide, 3),
            StructureRotation(bakery_wall_counter, 2),
            StructureRotation(bakery_wall_narrow, 3),
            StructureRotation(bakery_wall_wide, 3),  
        ],
    ),
    bakery_corner_narrow_to_narrow: StructureAdjacency(
        structure_name=bakery_corner_narrow_to_narrow,
        x_minus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 1),
            StructureRotation(bakery_corner_wide_to_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_entrance_open, 0),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_wall_counter, 0),
            StructureRotation(bakery_wall_narrow, 1),
        ],
        z_minus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 3),
            StructureRotation(bakery_corner_narrow_to_wide, 3),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_oven_narrow, 0),
            StructureRotation(bakery_wall_counter, 3),
            StructureRotation(bakery_wall_narrow, 0),
        ]
    ),
    bakery_corner_narrow_to_wide: StructureAdjacency(
        structure_name=bakery_corner_narrow_to_wide,
        x_minus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 1),
            StructureRotation(bakery_corner_wide_to_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_entrance_open, 0),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_wall_counter, 0),
            StructureRotation(bakery_wall_narrow, 1),
        ],
        z_minus=[
            StructureRotation(bakery_corner_wide_to_wide, 1),
            StructureRotation(bakery_corner_wide_to_narrow, 2),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_corridor_to_left, 3),
            StructureRotation(bakery_corridor_to_open, 3),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_wide, 0),
        ]
    ),
    bakery_corner_wide_to_narrow: StructureAdjacency(
        structure_name=bakery_corner_wide_to_narrow,
        x_plus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 0),
            StructureRotation(bakery_corner_narrow_to_wide, 0),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_wall_counter, 0),
            StructureRotation(bakery_wall_narrow, 1),
        ],
        z_minus=[
            StructureRotation(bakery_corner_narrow_to_wide, 2),
            StructureRotation(bakery_corner_wide_to_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            StructureRotation(bakery_corridor_to_right, 1),
            StructureRotation(bakery_corridor_to_open, 1),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_wide, 2),
        ],
    ),
    bakery_corner_wide_to_wide: StructureAdjacency(
        structure_name=bakery_corner_wide_to_wide,
        x_plus=[
            StructureRotation(bakery_corner_wide_to_wide, 1),
            StructureRotation(bakery_corner_narrow_to_wide, 3),
            StructureRotation(bakery_corridor_to_left, 3),
            StructureRotation(bakery_corridor_to_right, 2),
            StructureRotation(bakery_corridor_to_open, 2),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_oven_wide, 3),
            StructureRotation(bakery_wall_wide, 3),
        ],
        z_plus=[
            StructureRotation(bakery_corner_wide_to_wide, 3),
            StructureRotation(bakery_corner_wide_to_narrow, 0),
            StructureRotation(bakery_corridor_to_left, 2),
            StructureRotation(bakery_corridor_to_right, 1),
            StructureRotation(bakery_corridor_to_open, 0),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_entrance_open, 1),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_wide, 2),
        ],
    ),
    bakery_corridor_corner: StructureAdjacency(
        structure_name=bakery_corridor_corner,
        x_minus=[
            StructureRotation(bakery_corridor_corner, 2),
            StructureRotation(bakery_corridor_corner, 3),
            StructureRotation(bakery_corridor_end, 1),
            StructureRotation(bakery_corridor_entrance, 1),
            StructureRotation(bakery_corridor_straight, 1),
            StructureRotation(bakery_corridor_straight, 3),
            StructureRotation(bakery_corridor_to_left, 3),
            StructureRotation(bakery_corridor_to_right, 3),
            StructureRotation(bakery_corridor_to_open, 3),
        ],
        z_plus=[
            StructureRotation(bakery_corridor_corner, 1),
            StructureRotation(bakery_corridor_corner, 2),
            StructureRotation(bakery_corridor_end, 0),
            StructureRotation(bakery_corridor_entrance, 0),
            StructureRotation(bakery_corridor_straight, 0),
            StructureRotation(bakery_corridor_straight, 2),
            StructureRotation(bakery_corridor_to_left, 2),
            StructureRotation(bakery_corridor_to_right, 2),
            StructureRotation(bakery_corridor_to_open, 2),
        ]
    ),
    bakery_corridor_end: StructureAdjacency(
        structure_name=bakery_corridor_end,
        z_minus=[
            StructureRotation(bakery_corridor_corner, 0),
            StructureRotation(bakery_corridor_corner, 3),
            StructureRotation(bakery_corridor_entrance, 2),
            StructureRotation(bakery_corridor_straight, 0),
            StructureRotation(bakery_corridor_straight, 2),
            StructureRotation(bakery_corridor_to_left, 0),
            StructureRotation(bakery_corridor_to_right, 0),
            StructureRotation(bakery_corridor_to_open, 0),
        ]
    ),
    bakery_corridor_entrance: StructureAdjacency(
        structure_name=bakery_corridor_entrance,
        z_minus=[
            StructureRotation(bakery_corridor_corner, 0),
            StructureRotation(bakery_corridor_corner, 3),
            StructureRotation(bakery_corridor_end, 2),
            StructureRotation(bakery_corridor_straight, 0),
            StructureRotation(bakery_corridor_straight, 2),
            StructureRotation(bakery_corridor_to_left, 0),
            StructureRotation(bakery_corridor_to_right, 0),
            StructureRotation(bakery_corridor_to_open, 0),
        ]
    ),
    bakery_corridor_straight: StructureAdjacency(
        structure_name=bakery_corridor_straight,
        z_plus=[
            StructureRotation(bakery_corridor_corner, 1),
            StructureRotation(bakery_corridor_corner, 2),
            StructureRotation(bakery_corridor_end, 0),
            StructureRotation(bakery_corridor_entrance, 0),
            StructureRotation(bakery_corridor_straight, 0),
            StructureRotation(bakery_corridor_straight, 2),
            StructureRotation(bakery_corridor_to_left, 2),
            StructureRotation(bakery_corridor_to_right, 2),
            StructureRotation(bakery_corridor_to_open, 2),
        ],
        z_minus=[
            StructureRotation(bakery_corridor_corner, 0),
            StructureRotation(bakery_corridor_corner, 3),
            StructureRotation(bakery_corridor_end, 2),
            StructureRotation(bakery_corridor_straight, 0),
            StructureRotation(bakery_corridor_straight, 2),
            StructureRotation(bakery_corridor_to_left, 0),
            StructureRotation(bakery_corridor_to_right, 0),
            StructureRotation(bakery_corridor_to_open, 0),
        ]
    ),
    bakery_corridor_to_left: StructureAdjacency(
        structure_name=bakery_corridor_to_left,
        x_minus=[
            StructureRotation(bakery_corner_narrow_to_wide, 1),
            StructureRotation(bakery_corner_wide_to_wide, 3),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_oven_wide, 1),
            StructureRotation(bakery_wall_wide, 1),
        ],
        z_plus=[
            StructureRotation(bakery_corridor_corner, 1),
            StructureRotation(bakery_corridor_corner, 2),
            StructureRotation(bakery_corridor_end, 0),
            StructureRotation(bakery_corridor_entrance, 0),
            StructureRotation(bakery_corridor_straight, 0),
            StructureRotation(bakery_corridor_straight, 2),
            StructureRotation(bakery_corridor_to_left, 2),
            StructureRotation(bakery_corridor_to_right, 2),
            StructureRotation(bakery_corridor_to_open, 2),
        ],
        z_minus=[
            StructureRotation(bakery_corner_wide_to_wide, 1),
            StructureRotation(bakery_corner_wide_to_narrow, 2),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_corridor_to_left, 3),
            StructureRotation(bakery_corridor_to_open, 3),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_wide, 0),
        ],
    ),
    bakery_corridor_to_open: StructureAdjacency(
        structure_name=bakery_corridor_to_open,
        x_plus=[
            StructureRotation(bakery_corner_wide_to_narrow, 3),
            StructureRotation(bakery_corner_wide_to_wide, 2),
            StructureRotation(bakery_entrance_open, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            StructureRotation(bakery_oven_wide, 1),
            StructureRotation(bakery_wall_wide, 1),
        ],
        x_minus=[
            StructureRotation(bakery_corner_narrow_to_wide, 1),
            StructureRotation(bakery_corner_wide_to_wide, 3),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_oven_wide, 1),
            StructureRotation(bakery_wall_wide, 1),
        ],
        z_plus=[
            StructureRotation(bakery_corridor_corner, 1),
            StructureRotation(bakery_corridor_corner, 2),
            StructureRotation(bakery_corridor_end, 0),
            StructureRotation(bakery_corridor_entrance, 0),
            StructureRotation(bakery_corridor_straight, 0),
            StructureRotation(bakery_corridor_straight, 2),
            StructureRotation(bakery_corridor_to_left, 2),
            StructureRotation(bakery_corridor_to_right, 2),
            StructureRotation(bakery_corridor_to_open, 2),
        ],
        z_minus=[
            StructureRotation(bakery_corridor_to_open, 2),
            StructureRotation(bakery_entrance_open, 2),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 1),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 1),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 3),
            StructureRotation(bakery_wall_narrow, 3),
            StructureRotation(bakery_oven_wide, 3),
            StructureRotation(bakery_wall_wide, 3),
            StructureRotation(bakery_wall_counter,2),
        ]
    ),
    bakery_corridor_to_right: StructureAdjacency(
        structure_name=bakery_corridor_to_right,
        x_plus=[
            StructureRotation(bakery_corner_wide_to_narrow, 3),
            StructureRotation(bakery_corner_wide_to_wide, 2),
            StructureRotation(bakery_entrance_open, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            StructureRotation(bakery_oven_wide, 1),
            StructureRotation(bakery_wall_wide, 1),
        ],
        z_plus=[
            StructureRotation(bakery_corridor_corner, 1),
            StructureRotation(bakery_corridor_corner, 2),
            StructureRotation(bakery_corridor_end, 0),
            StructureRotation(bakery_corridor_entrance, 0),
            StructureRotation(bakery_corridor_straight, 0),
            StructureRotation(bakery_corridor_straight, 2),
            StructureRotation(bakery_corridor_to_left, 2),
            StructureRotation(bakery_corridor_to_right, 2),
            StructureRotation(bakery_corridor_to_open, 2),
        ],
        z_minus=[
            StructureRotation(bakery_corner_narrow_to_wide, 2),
            StructureRotation(bakery_corner_wide_to_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            StructureRotation(bakery_corridor_to_right, 1),
            StructureRotation(bakery_corridor_to_open, 1),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_wide, 2),
        ],
    ),
    bakery_entrance_open: StructureAdjacency(
        structure_name=bakery_entrance_open,
        x_plus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 0),
            StructureRotation(bakery_corner_narrow_to_wide, 0),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_wall_counter, 0),
            StructureRotation(bakery_wall_narrow, 1),
        ],
        x_minus=[
            StructureRotation(bakery_corner_narrow_to_wide, 1),
            StructureRotation(bakery_corner_wide_to_wide, 3),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_oven_wide, 1),
            StructureRotation(bakery_wall_wide, 1),
        ],
        z_minus=[
            StructureRotation(bakery_corridor_to_open, 2),
            StructureRotation(bakery_entrance_open, 2),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 1),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 1),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 3),
            StructureRotation(bakery_wall_narrow, 3),
            StructureRotation(bakery_oven_wide, 3),
            StructureRotation(bakery_wall_wide, 3),
            StructureRotation(bakery_wall_counter,2),
        ]
    ),
    bakery_inner_corner_wide: StructureAdjacency(
        structure_name=bakery_inner_corner_wide,
        x_plus=[
            StructureRotation(bakery_corridor_to_open, 3),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_inner_corner_narrow, 1),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_inner_corner_wide, 1),
            StructureRotation(bakery_inner_corner_wide, 2),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 0),
            StructureRotation(bakery_wall_narrow, 0),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_wide, 0),
            StructureRotation(bakery_wall_counter,3),
        ],
        x_minus=[
            StructureRotation(bakery_corner_wide_to_narrow, 1),
            StructureRotation(bakery_corner_wide_to_wide, 0),
            StructureRotation(bakery_corridor_to_left, 2),
            StructureRotation(bakery_corridor_to_open, 2),
            StructureRotation(bakery_oven_wide, 3),
            StructureRotation(bakery_wall_wide, 3),
            StructureRotation(bakery_entrance_open, 2),
        ],
        z_plus=[
            StructureRotation(bakery_corridor_to_open, 0),
            StructureRotation(bakery_entrance_open, 0),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_inner_corner_wide, 3),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_wall_narrow, 1),
            StructureRotation(bakery_oven_wide, 1),
            StructureRotation(bakery_wall_wide, 1),
            StructureRotation(bakery_wall_counter,0),
        ],
        z_minus=[
            StructureRotation(bakery_corner_narrow_to_wide, 2),
            StructureRotation(bakery_corner_wide_to_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            StructureRotation(bakery_corridor_to_right, 1),
            StructureRotation(bakery_corridor_to_open, 1),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_wide, 2),
        ]
    ),
    bakery_inner_corner_narrow: StructureAdjacency(
        structure_name=bakery_inner_corner_narrow,
        x_plus=[
            StructureRotation(bakery_corridor_to_open, 3),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_inner_corner_narrow, 1),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_inner_corner_wide, 1),
            StructureRotation(bakery_inner_corner_wide, 2),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 0),
            StructureRotation(bakery_wall_narrow, 0),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_wide, 0),
            StructureRotation(bakery_wall_counter,3),
        ],
        x_minus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 2),
            StructureRotation(bakery_corner_narrow_to_wide, 2),
            StructureRotation(bakery_oven_narrow, 3),
            StructureRotation(bakery_wall_narrow, 3),
            StructureRotation(bakery_wall_counter,2),
        ],
        z_plus=[
            StructureRotation(bakery_corridor_to_open, 0),
            StructureRotation(bakery_entrance_open, 0),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_inner_corner_wide, 3),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_wall_narrow, 1),
            StructureRotation(bakery_oven_wide, 1),
            StructureRotation(bakery_wall_wide, 1),
            StructureRotation(bakery_wall_counter,0),
        ],
        z_minus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 2),
            StructureRotation(bakery_corner_wide_to_narrow, 1),
            StructureRotation(bakery_oven_narrow, 2),
            StructureRotation(bakery_wall_narrow, 2),
            StructureRotation(bakery_wall_counter,1),
        ]
    ),
    bakery_middle_chairs: StructureAdjacency(
        structure_name=bakery_middle_chairs,
        x_plus=[
            StructureRotation(bakery_corridor_to_open, 3),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_inner_corner_narrow, 1),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_inner_corner_wide, 1),
            StructureRotation(bakery_inner_corner_wide, 2),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 0),
            StructureRotation(bakery_wall_narrow, 0),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_wide, 0),
            StructureRotation(bakery_wall_counter,3),
        ],
        x_minus=[
            StructureRotation(bakery_corridor_to_open, 1),
            StructureRotation(bakery_entrance_open, 1),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 2),
            StructureRotation(bakery_wall_narrow, 2),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_wide, 2),
            StructureRotation(bakery_wall_counter,1),
        ],
        z_plus=[
            StructureRotation(bakery_corridor_to_open, 0),
            StructureRotation(bakery_entrance_open, 0),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_inner_corner_wide, 3),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_wall_narrow, 1),
            StructureRotation(bakery_oven_wide, 1),
            StructureRotation(bakery_wall_wide, 1),
            StructureRotation(bakery_wall_counter,0),
        ],
        z_minus=[
            StructureRotation(bakery_corridor_to_open, 2),
            StructureRotation(bakery_entrance_open, 2),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 1),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 1),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 3),
            StructureRotation(bakery_wall_narrow, 3),
            StructureRotation(bakery_oven_wide, 3),
            StructureRotation(bakery_wall_wide, 3),
            StructureRotation(bakery_wall_counter,2),
        ]
    ),
    bakery_middle_counter: StructureAdjacency(
        structure_name=bakery_middle_counter,
        x_plus=[
            StructureRotation(bakery_corridor_to_open, 3),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_inner_corner_narrow, 1),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_inner_corner_wide, 1),
            StructureRotation(bakery_inner_corner_wide, 2),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 0),
            StructureRotation(bakery_wall_narrow, 0),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_wide, 0),
            StructureRotation(bakery_wall_counter,3),
        ],
        x_minus=[
            StructureRotation(bakery_corridor_to_open, 1),
            StructureRotation(bakery_entrance_open, 1),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 2),
            StructureRotation(bakery_wall_narrow, 2),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_wide, 2),
            StructureRotation(bakery_wall_counter,1),
        ],
        z_plus=[
            StructureRotation(bakery_corridor_to_open, 0),
            StructureRotation(bakery_entrance_open, 0),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_inner_corner_wide, 3),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_wall_narrow, 1),
            StructureRotation(bakery_oven_wide, 1),
            StructureRotation(bakery_wall_wide, 1),
            StructureRotation(bakery_wall_counter,0),
        ],
        z_minus=[
            StructureRotation(bakery_corridor_to_open, 2),
            StructureRotation(bakery_entrance_open, 2),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 1),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 1),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 3),
            StructureRotation(bakery_wall_narrow, 3),
            StructureRotation(bakery_oven_wide, 3),
            StructureRotation(bakery_wall_wide, 3),
            StructureRotation(bakery_wall_counter,2),
        ]
    ),
    bakery_oven_narrow: StructureAdjacency(
        structure_name=bakery_oven_narrow,
        x_minus=[
            StructureRotation(bakery_corridor_to_open, 1),
            StructureRotation(bakery_entrance_open, 1),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 2),
            StructureRotation(bakery_wall_narrow, 2),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_wide, 2),
            StructureRotation(bakery_wall_counter,1),
        ],
        z_plus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 0),
            StructureRotation(bakery_corner_wide_to_narrow, 3),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_oven_narrow, 0),
            StructureRotation(bakery_wall_narrow, 0),
            StructureRotation(bakery_wall_counter,3),
        ],
        z_minus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 3),
            StructureRotation(bakery_corner_narrow_to_wide, 3),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_oven_narrow, 0),
            StructureRotation(bakery_wall_counter, 3),
            StructureRotation(bakery_wall_narrow, 0),
        ]
    ),
    bakery_oven_wide: StructureAdjacency(
        structure_name=bakery_oven_wide,
        x_minus=[
            StructureRotation(bakery_corridor_to_open, 1),
            StructureRotation(bakery_entrance_open, 1),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 2),
            StructureRotation(bakery_wall_narrow, 2),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_wide, 2),
            StructureRotation(bakery_wall_counter,1),
        ],
        z_plus=[
            StructureRotation(bakery_corner_narrow_to_wide, 0),
            StructureRotation(bakery_corner_wide_to_wide, 2),
            StructureRotation(bakery_corridor_to_left, 0),
            StructureRotation(bakery_corridor_to_open, 3),
            StructureRotation(bakery_corridor_to_right, 3),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_wide, 0),
        ],
        z_minus=[
            StructureRotation(bakery_corner_wide_to_wide, 1),
            StructureRotation(bakery_corner_wide_to_narrow, 2),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_corridor_to_left, 3),
            StructureRotation(bakery_corridor_to_open, 3),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_wide, 0),
        ],
    ),
    bakery_wall_counter: StructureAdjacency(
        structure_name=bakery_wall_counter,
        x_plus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 0),
            StructureRotation(bakery_corner_narrow_to_wide, 0),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_wall_counter, 0),
            StructureRotation(bakery_wall_narrow, 1),
        ],
        x_minus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 1),
            StructureRotation(bakery_corner_wide_to_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_entrance_open, 0),
            StructureRotation(bakery_oven_narrow, 1),
            StructureRotation(bakery_wall_counter, 0),
            StructureRotation(bakery_wall_narrow, 1),
        ],
        z_minus=[
            StructureRotation(bakery_corridor_to_open, 2),
            StructureRotation(bakery_entrance_open, 2),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 1),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 1),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 3),
            StructureRotation(bakery_wall_narrow, 3),
            StructureRotation(bakery_oven_wide, 3),
            StructureRotation(bakery_wall_wide, 3),
            StructureRotation(bakery_wall_counter,2),
        ]
    ),
    bakery_wall_narrow: StructureAdjacency(
        structure_name=bakery_wall_narrow,
        x_minus=[
            StructureRotation(bakery_corridor_to_open, 1),
            StructureRotation(bakery_entrance_open, 1),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 2),
            StructureRotation(bakery_wall_narrow, 2),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_wide, 2),
            StructureRotation(bakery_wall_counter,1),
        ],
        z_plus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 0),
            StructureRotation(bakery_corner_wide_to_narrow, 3),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_oven_narrow, 0),
            StructureRotation(bakery_wall_narrow, 0),
            StructureRotation(bakery_wall_counter,3),
        ],
        z_minus=[
            StructureRotation(bakery_corner_narrow_to_narrow, 3),
            StructureRotation(bakery_corner_narrow_to_wide, 3),
            StructureRotation(bakery_inner_corner_narrow, 2),
            StructureRotation(bakery_oven_narrow, 0),
            StructureRotation(bakery_wall_counter, 3),
            StructureRotation(bakery_wall_narrow, 0),
        ]
    ),
    bakery_wall_wide: StructureAdjacency(
        structure_name=bakery_wall_wide,
        x_minus=[
            StructureRotation(bakery_corridor_to_open, 1),
            StructureRotation(bakery_entrance_open, 1),
            StructureRotation(bakery_inner_corner_narrow, 0),
            StructureRotation(bakery_inner_corner_narrow, 3),
            StructureRotation(bakery_inner_corner_wide, 0),
            StructureRotation(bakery_inner_corner_wide, 3),
            *all_rotations(bakery_middle_chairs),
            *all_rotations(bakery_middle_counter),
            StructureRotation(bakery_oven_narrow, 2),
            StructureRotation(bakery_wall_narrow, 2),
            StructureRotation(bakery_oven_wide, 2),
            StructureRotation(bakery_wall_wide, 2),
            StructureRotation(bakery_wall_counter,1),
        ],
        z_plus=[
            StructureRotation(bakery_corner_narrow_to_wide, 0),
            StructureRotation(bakery_corner_wide_to_wide, 2),
            StructureRotation(bakery_corridor_to_left, 0),
            StructureRotation(bakery_corridor_to_open, 3),
            StructureRotation(bakery_corridor_to_right, 3),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_wide, 0),
        ],
        z_minus=[
            StructureRotation(bakery_corner_wide_to_wide, 1),
            StructureRotation(bakery_corner_wide_to_narrow, 2),
            StructureRotation(bakery_inner_corner_wide, 2),
            StructureRotation(bakery_corridor_to_left, 3),
            StructureRotation(bakery_corridor_to_open, 3),
            StructureRotation(bakery_entrance_open, 3),
            StructureRotation(bakery_oven_wide, 0),
            StructureRotation(bakery_wall_wide, 0),
        ],
    ),
}