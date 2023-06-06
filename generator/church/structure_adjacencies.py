import logging

from generator.church.structures import (
    church_altar,
    churchcorner_altar_left,
    churchcorner_altar_right,
    churchcorner_straight,
    churchentrance,
    churchstraight_no_altar,
    churchstraight_to_altar,
    empty_space_air,
)
from generator.utils.structure_adjacency import StructureAdjacency, all_rotations, check_symmetry
from generator.utils.structure_rotation import StructureRotation

logger = logging.getLogger(__name__)

structure_adjecencies = {
    empty_space_air: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=empty_space_air,
        x_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(church_altar, 0),
            StructureRotation(church_altar, 2),
            StructureRotation(church_altar, 3),
            StructureRotation(churchcorner_altar_left, 2),
            StructureRotation(churchcorner_altar_left, 3),
            StructureRotation(churchcorner_altar_right, 0),
            StructureRotation(churchcorner_altar_right, 3),
            StructureRotation(churchcorner_straight, 0),
            StructureRotation(churchcorner_straight, 3),
            StructureRotation(churchentrance, 0),
            StructureRotation(churchentrance, 1),
            StructureRotation(churchentrance, 2),
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_no_altar, 2),
            StructureRotation(churchstraight_to_altar, 0),
            StructureRotation(churchstraight_to_altar, 2),
        ],
        z_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(church_altar, 1),
            StructureRotation(church_altar, 2),
            StructureRotation(church_altar, 3),
            StructureRotation(churchcorner_altar_left, 1),
            StructureRotation(churchcorner_altar_left, 2),
            StructureRotation(churchcorner_altar_right, 2),
            StructureRotation(churchcorner_altar_right, 3),
            StructureRotation(churchcorner_straight, 2),
            StructureRotation(churchcorner_straight, 3),
            StructureRotation(churchentrance, 0),
            StructureRotation(churchentrance, 1),
            StructureRotation(churchentrance, 3),
            StructureRotation(churchstraight_no_altar, 1),
            StructureRotation(churchstraight_no_altar, 3),
            StructureRotation(churchstraight_to_altar, 1),
            StructureRotation(churchstraight_to_altar, 3),
        ],
        x_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(church_altar, 0),
            StructureRotation(church_altar, 1),
            StructureRotation(church_altar, 2),
            StructureRotation(churchcorner_altar_left, 0),
            StructureRotation(churchcorner_altar_left, 1),
            StructureRotation(churchcorner_altar_right, 1),
            StructureRotation(churchcorner_altar_right, 2),
            StructureRotation(churchcorner_straight, 1),
            StructureRotation(churchcorner_straight, 2),
            StructureRotation(churchentrance, 0),
            StructureRotation(churchentrance, 2),
            StructureRotation(churchentrance, 3),
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_no_altar, 2),
            StructureRotation(churchstraight_to_altar, 0),
            StructureRotation(churchstraight_to_altar, 2),
        ],
        z_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(church_altar, 0),
            StructureRotation(church_altar, 1),
            StructureRotation(church_altar, 3),
            StructureRotation(churchcorner_altar_left, 0),
            StructureRotation(churchcorner_altar_left, 3),
            StructureRotation(churchcorner_altar_right, 0),
            StructureRotation(churchcorner_altar_right, 1),
            StructureRotation(churchcorner_straight, 0),
            StructureRotation(churchcorner_straight, 1),
            StructureRotation(churchentrance, 1),
            StructureRotation(churchentrance, 2),
            StructureRotation(churchentrance, 3),
            StructureRotation(churchstraight_no_altar, 1),
            StructureRotation(churchstraight_no_altar, 3),
            StructureRotation(churchstraight_to_altar, 1),
            StructureRotation(churchstraight_to_altar, 3),
        ],
    ),
    church_altar: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=church_altar,
        z_minus=[
            StructureRotation(churchcorner_altar_left, 1),
            StructureRotation(churchcorner_altar_right, 3),
            StructureRotation(churchentrance, 0),
            StructureRotation(churchstraight_to_altar, 0),
        ],
    ),
    churchcorner_altar_left: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchcorner_altar_left,
        x_plus=[StructureRotation(church_altar, 3), StructureRotation(churchstraight_to_altar, 3)],
        z_minus=[StructureRotation(churchstraight_no_altar, 0)],
    ),
    churchcorner_altar_right: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchcorner_altar_right,
        x_minus=[
            StructureRotation(church_altar, 1),
            StructureRotation(churchstraight_to_altar, 1),
        ],
        z_minus=[
            StructureRotation(churchentrance, 0),
            StructureRotation(churchstraight_no_altar, 0),
        ],
    ),
    churchcorner_straight: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchcorner_straight,
        x_minus=[
            StructureRotation(churchstraight_no_altar, 1),
            StructureRotation(churchstraight_to_altar, 1),
        ],
        z_minus=[
            StructureRotation(churchentrance, 0),
            StructureRotation(churchstraight_no_altar, 0),
        ],
    ),
    churchentrance: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchentrance,
        z_plus=[
            StructureRotation(church_altar, 0),
            StructureRotation(churchcorner_altar_right, 0),
            StructureRotation(churchcorner_straight, 0),
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_to_altar, 0),
        ],
    ),
    churchstraight_no_altar: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchstraight_no_altar,
        z_plus=[
            StructureRotation(churchcorner_altar_left, 0),
            StructureRotation(churchcorner_altar_right, 0),
            StructureRotation(churchcorner_straight, 0),
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_to_altar, 0),
        ],
        z_minus=[
            StructureRotation(churchentrance, 0),
            StructureRotation(churchcorner_straight, 3),
            StructureRotation(churchstraight_no_altar, 0),
        ],
    ),
    churchstraight_to_altar: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchstraight_to_altar,
        z_plus=[
            StructureRotation(churchstraight_to_altar, 0),
            StructureRotation(church_altar, 0),
        ],
        z_minus=[
            StructureRotation(churchcorner_altar_left, 1),
            StructureRotation(churchcorner_altar_right, 3),
            StructureRotation(churchcorner_straight, 3),
            StructureRotation(churchentrance, 0),
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_to_altar, 0),
        ],
    ),
}

if __name__ == "__main__":
    print(structure_adjecencies[church_altar].adjecent_structrues("z_minus", 3))

    check_symmetry(structure_adjecencies)
