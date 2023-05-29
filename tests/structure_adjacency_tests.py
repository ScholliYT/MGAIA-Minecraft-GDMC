import unittest

import assignment.bakery.structure_adjacencies as bakery
import assignment.brickhouse.structure_adjacencies as brickhouse
import assignment.church.structure_adjacencies as church
import assignment.farm.structure_adjacencies as farm
from assignment.utils.structure_adjacency import check_symmetry


class TestSymmetryChecker(unittest.TestCase):
    def test_brickhouse_structure_adjecencies_symmetry(self):
        check_symmetry(brickhouse.structure_adjecencies)

    def test_bakery_structure_adjecencies_symmetry(self):
        check_symmetry(
            bakery.structure_adjecencies,
            structure_subset=set(
                [
                    bakery.empty_space_air,
                    bakery.bakery_corner_narrow_to_narrow,
                    bakery.bakery_corner_narrow_to_wide,
                    bakery.bakery_corner_wide_to_narrow,
                    bakery.bakery_corner_wide_to_wide,
                    bakery.bakery_corridor_corner,
                    bakery.bakery_corridor_end,
                    bakery.bakery_corridor_entrance,
                    # bakery.bakery_corridor_straight, # broken
                    # bakery.bakery_corridor_to_left, # broken
                    # bakery.bakery_corridor_to_open, # broken
                    # bakery.bakery_corridor_to_right, # broken
                    bakery.bakery_entrance_open,
                    # bakery.bakery_inner_corner_wide, # broken
                    # bakery.bakery_inner_corner_narrow, # broken
                    bakery.bakery_middle_chairs,
                    bakery.bakery_middle_counter,
                    bakery.bakery_oven_narrow,
                    bakery.bakery_oven_wide,
                    bakery.bakery_wall_counter,
                    bakery.bakery_wall_narrow,
                    bakery.bakery_wall_wide,
                ]
            ),
        )

    def test_farm_structure_adjecencies_symmetry(self):
        check_symmetry(farm.structure_adjecencies)

    def test_church_structure_adjecencies_symmetry(self):
        check_symmetry(church.structure_adjecencies)
