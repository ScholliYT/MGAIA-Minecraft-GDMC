import unittest

import assignment.bakery.structure_adjacencies as bakery
import assignment.brickhouse.structure_adjacencies as brickhouse
import assignment.church.structure_adjacencies as church
import assignment.farm.structure_adjacencies as farm
import assignment.school.structure_adjacencies as school
from assignment.utils.structure_adjacency import check_symmetry


class TestSymmetryChecker(unittest.TestCase):
    def test_brickhouse_structure_adjecencies_symmetry(self):
        check_symmetry(brickhouse.structure_adjecencies)

    def test_bakery_structure_adjecencies_symmetry(self):
        check_symmetry(bakery.structure_adjecencies)

    def test_farm_structure_adjecencies_symmetry(self):
        check_symmetry(farm.structure_adjecencies)

    def test_church_structure_adjecencies_symmetry(self):
        check_symmetry(church.structure_adjecencies)

    def test_school_structure_adjecencies_symmetry(self):
        check_symmetry(school.structure_adjecencies)
