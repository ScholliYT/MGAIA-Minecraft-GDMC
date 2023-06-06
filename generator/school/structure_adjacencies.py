# import sys
# import os

# parent_directory = r'C:\Users\sbone\Documents\Leiden Masters\YR1\SEM2\Modern Game AI Algorithms\Assignment 3\Bakery\MGAIA-Minecraft-GDMC-bakery'
# sys.path.append(os.path.abspath(parent_directory))


import logging

from generator.school.structures import (
    empty_space_air,
    school_cafeteria,
    school_classroom,
    school_corner,
    school_entrance,
    school_library,
    school_lower_stairs,
    school_roof,
    school_upper_entrance,
    school_upper_middle,
    school_upper_stairs,
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
            StructureRotation(school_classroom, 1),
            StructureRotation(school_corner, 1),
            StructureRotation(school_corner, 2),
            StructureRotation(school_entrance, 1),
            StructureRotation(school_library, 2),
            StructureRotation(school_lower_stairs, 2),
            StructureRotation(school_lower_stairs, 3),
            ##roofs??
            StructureRotation(school_upper_entrance, 1),
            StructureRotation(school_upper_stairs, 2),
            StructureRotation(school_upper_stairs, 3),
            # StructureRotation(school_roof, 0)
        ],
        z_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(school_classroom, 0),
            StructureRotation(school_corner, 0),
            StructureRotation(school_corner, 1),
            StructureRotation(school_entrance, 0),
            StructureRotation(school_library, 1),
            StructureRotation(school_lower_stairs, 1),
            StructureRotation(school_lower_stairs, 2),
            # roofs??
            StructureRotation(school_upper_entrance, 0),
            StructureRotation(school_upper_stairs, 1),
            StructureRotation(school_upper_stairs, 2),
            # StructureRotation(school_roof, 0)
        ],
        x_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(school_classroom, 3),
            StructureRotation(school_corner, 0),
            StructureRotation(school_corner, 3),
            StructureRotation(school_entrance, 3),
            StructureRotation(school_library, 0),
            StructureRotation(school_lower_stairs, 0),
            StructureRotation(school_lower_stairs, 1),
            # #roofs??
            StructureRotation(school_upper_entrance, 3),
            StructureRotation(school_upper_stairs, 0),
            StructureRotation(school_upper_stairs, 1),
            # StructureRotation(school_roof, 0)
        ],
        z_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(school_classroom, 2),
            StructureRotation(school_corner, 2),
            StructureRotation(school_corner, 3),
            StructureRotation(school_entrance, 2),
            StructureRotation(school_library, 3),
            StructureRotation(school_lower_stairs, 0),
            StructureRotation(school_lower_stairs, 3),
            # #roofs??
            StructureRotation(school_upper_entrance, 2),
            StructureRotation(school_upper_stairs, 0),
            StructureRotation(school_upper_stairs, 3),
            # StructureRotation(school_roof, 0)
        ],
        y_plus=[*all_rotations(empty_space_air)],
        y_minus=[*all_rotations(empty_space_air)]
        # ,  StructureRotation(school_roof, 0)
        # roofs?
    ),
    school_cafeteria: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=school_cafeteria,
        x_minus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_library, 0),
        ],
        z_plus=[
            StructureRotation(school_classroom, 2),
            StructureRotation(school_library, 3),
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_entrance, 2),
            StructureRotation(school_upper_entrance, 2),
        ],
        x_plus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_library, 2),
        ],
        z_minus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_classroom, 0),
            StructureRotation(school_entrance, 0),
            StructureRotation(school_upper_entrance, 0),
            # school entrance roof
            StructureRotation(school_library, 1),
        ],
        y_plus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_roof, 0),
        ],
        y_minus=[StructureRotation(school_cafeteria, 0)],
    ),
    school_classroom: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=school_classroom,
        z_plus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_cafeteria, 2),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_upper_middle, 2),
            StructureRotation(school_library, 0),
            StructureRotation(school_library, 3),
            StructureRotation(school_corner, 3),
            StructureRotation(school_lower_stairs, 0),
            StructureRotation(school_upper_stairs, 0),
        ],
        x_minus=[
            StructureRotation(school_corner, 0),
            StructureRotation(school_lower_stairs, 1),
            StructureRotation(school_upper_stairs, 1),
            StructureRotation(school_entrance, 0),
            StructureRotation(school_upper_entrance, 0),
            StructureRotation(school_library, 1),
        ],
        x_plus=[
            StructureRotation(school_corner, 1),
            StructureRotation(school_lower_stairs, 2),
            StructureRotation(school_upper_stairs, 2),
            StructureRotation(school_entrance, 0),
            StructureRotation(school_upper_entrance, 0),
            StructureRotation(school_library, 1),
        ],
        y_plus=[StructureRotation(school_classroom, 0), StructureRotation(school_roof, 0)],
        y_minus=[StructureRotation(school_classroom, 0)],
    ),
    school_corner: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=school_corner,
        x_plus=[
            StructureRotation(school_classroom, 0),
            StructureRotation(school_classroom, 1),
            StructureRotation(school_corner, 1),
            StructureRotation(school_lower_stairs, 2),
            StructureRotation(school_upper_stairs, 2),
            StructureRotation(school_entrance, 1),
            StructureRotation(school_upper_entrance, 1),
            StructureRotation(school_library, 1),
        ],
        z_plus=[
            StructureRotation(school_library, 0),
            StructureRotation(school_entrance, 2),
            StructureRotation(school_upper_entrance, 2),
            StructureRotation(school_corner, 3),
            StructureRotation(school_lower_stairs, 0),
            StructureRotation(school_upper_stairs, 0),
            StructureRotation(school_classroom, 3),
        ],
        y_plus=[StructureRotation(school_corner, 0), StructureRotation(school_roof, 0)],
        y_minus=[StructureRotation(school_corner, 0)],
    ),
    school_entrance: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=school_entrance,
        x_plus=[StructureRotation(school_classroom, 0)],
        x_minus=[StructureRotation(school_classroom, 0)],
        z_plus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_cafeteria, 2),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_upper_middle, 2),
            StructureRotation(school_library, 3),
            StructureRotation(school_corner, 3),
            StructureRotation(school_corner, 2),
            StructureRotation(school_lower_stairs, 0),
            StructureRotation(school_lower_stairs, 3),
            StructureRotation(school_upper_stairs, 0),
            StructureRotation(school_upper_stairs, 3),
        ],
        y_plus=[StructureRotation(school_upper_entrance, 0)],
    ),
    school_library: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=school_library,
        x_plus=[
            StructureRotation(school_entrance, 1),
            StructureRotation(school_upper_entrance, 1),
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_cafeteria, 1),
            StructureRotation(school_cafeteria, 2),
            StructureRotation(school_cafeteria, 3),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_upper_middle, 1),
            StructureRotation(school_upper_middle, 2),
            StructureRotation(school_upper_middle, 3),
            StructureRotation(school_classroom, 1),
        ],
        z_minus=[
            StructureRotation(school_corner, 0),
            StructureRotation(school_lower_stairs, 1),
            StructureRotation(school_upper_stairs, 1),
            StructureRotation(school_library, 0),
            StructureRotation(school_classroom, 0),
            StructureRotation(school_classroom, 3),
        ],
        z_plus=[
            StructureRotation(school_library, 0),
            StructureRotation(school_corner, 3),
            StructureRotation(school_lower_stairs, 0),
            StructureRotation(school_upper_stairs, 0),
            StructureRotation(school_classroom, 3),
        ],
        y_plus=[StructureRotation(school_library, 0), StructureRotation(school_roof, 0)],
        y_minus=[StructureRotation(school_library, 0)],
    ),
    school_lower_stairs: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=school_lower_stairs,
        x_plus=[
            StructureRotation(school_classroom, 2),
            StructureRotation(school_corner, 2),
            StructureRotation(school_entrance, 1),
            StructureRotation(school_upper_entrance, 1),
            StructureRotation(school_library, 3),
        ],
        z_minus=[
            StructureRotation(school_library, 0),
            StructureRotation(school_entrance, 0),
            StructureRotation(school_upper_entrance, 0),
            StructureRotation(school_corner, 0),
            StructureRotation(school_classroom, 3),
            StructureRotation(school_classroom, 0),
        ],
        y_plus=[StructureRotation(school_upper_stairs, 0)],
    ),
    school_upper_entrance: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=school_upper_entrance,
        x_plus=[StructureRotation(school_classroom, 0)],
        x_minus=[StructureRotation(school_classroom, 0)],
        z_plus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_cafeteria, 2),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_upper_middle, 2),
            StructureRotation(school_library, 3),
            StructureRotation(school_corner, 3),
            StructureRotation(school_corner, 2),
            StructureRotation(school_lower_stairs, 0),
            StructureRotation(school_lower_stairs, 3),
            StructureRotation(school_upper_stairs, 0),
            StructureRotation(school_upper_stairs, 3),
        ],
        y_minus=[StructureRotation(school_entrance, 0)],
    ),
    school_upper_stairs: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=school_upper_stairs,
        x_plus=[
            StructureRotation(school_classroom, 2),
            StructureRotation(school_corner, 2),
            StructureRotation(school_entrance, 1),
            StructureRotation(school_upper_entrance, 1),
            StructureRotation(school_library, 3),
        ],
        z_minus=[
            StructureRotation(school_library, 0),
            StructureRotation(school_entrance, 0),
            StructureRotation(school_upper_entrance, 0),
            StructureRotation(school_corner, 0),
            StructureRotation(school_classroom, 3),
            StructureRotation(school_classroom, 0),
        ],
        y_minus=[StructureRotation(school_lower_stairs, 0)],
        y_plus=[StructureRotation(school_roof, 0)],
    ),
    school_upper_middle: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=school_upper_middle,
        x_minus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_library, 0),
        ],
        z_plus=[
            StructureRotation(school_classroom, 2),
            StructureRotation(school_library, 3),
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_entrance, 2),
            StructureRotation(school_upper_entrance, 2),
        ],
        x_plus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_library, 2),
        ],
        z_minus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_upper_middle, 0),
            StructureRotation(school_classroom, 0),
            StructureRotation(school_entrance, 0),
            StructureRotation(school_upper_entrance, 0),
            # school entrance roof
            StructureRotation(school_library, 1),
        ],
        # y_plus = [
        #     StructureRotation(school_cafeteria, 0),
        #     StructureRotation(school_upper_middle, 0),
        #     #StructureRotation(school_roof, 0)
        # ],
        y_plus=[StructureRotation(school_roof, 0)],
        y_minus=[StructureRotation(school_cafeteria, 0)],
    ),
    school_roof: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=school_roof,
        x_plus=[*all_rotations(school_roof)],
        x_minus=[*all_rotations(school_roof)],
        z_plus=[*all_rotations(school_roof)],
        z_minus=[*all_rotations(school_roof)],
        y_minus=[
            StructureRotation(school_cafeteria, 0),
            StructureRotation(school_classroom, 0),
            StructureRotation(school_corner, 0),
            StructureRotation(school_library, 0),
            StructureRotation(school_upper_stairs, 0),
            StructureRotation(school_upper_middle, 0),
        ],
    ),
}

if __name__ == "__main__":
    print(structure_adjecencies[school_entrance].adjecent_structrues("z_minus", 3))

    check_symmetry(structure_adjecencies)
