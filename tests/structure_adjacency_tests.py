import unittest

import generator.bakery.structure_adjacencies as bakery
import generator.brickhouse.structure_adjacencies as brickhouse
import generator.church.structure_adjacencies as church
import generator.farm.structure_adjacencies as farm
import generator.school.structure_adjacencies as school
from generator.utils.structure_adjacency import check_symmetry


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
