import unittest

from assignment.bakery.structure_adjacencies import (
    structure_adjecencies as bakery_structure_adjacencies,
)
from assignment.brickhouse.structure_adjacencies import (
    structure_adjecencies as brickhouse_structure_adjecencies,
)
from assignment.farm.structure_adjacencies import (
    structure_adjecencies as farm_structure_adjacencies,
)
from assignment.utils.structure_adjacency import check_symmetry


class TestSymmetryChecker(unittest.TestCase):
    def test_brickhouse_structure_adjecencies_symmetry(self):
        check_symmetry(brickhouse_structure_adjecencies)

    def test_bakery_structure_adjecencies_symmetry(self):
        check_symmetry(bakery_structure_adjacencies)
    
    def test_farm_structure_adjecencies_symmetry(self):
        check_symmetry(farm_structure_adjacencies)
