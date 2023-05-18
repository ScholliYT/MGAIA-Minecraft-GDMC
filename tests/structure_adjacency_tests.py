import unittest

from assignment.brickhouse.structure_adjacency import check_symmetry, structure_adjecencies


class TestSymmetryChecker(unittest.TestCase):
    def test_current_structure_adjecencies_symmetry(self):
        check_symmetry(structure_adjecencies)
