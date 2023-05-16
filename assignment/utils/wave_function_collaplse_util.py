from typing import List

from assignment.utils.structure_adjacency import StructureRotation
from assignment.utils.structures import (
    empty_space_air,
)
from assignment.utils.wave_function_collapse import WaveFunctionCollapse


def print_state(wfc: WaveFunctionCollapse):
    for y in range(wfc.state_space_size[1]):
        print("Layer y=" + str(y))
        for x in reversed(range(wfc.state_space_size[0])):
            for z in range(wfc.state_space_size[2]):
                print("{:02d}".format(len(wfc.state_space[x][y][z])), end=",")
            print()
        print()


def collapse_to_air_on_outer_rectangle(wfc: WaveFunctionCollapse):
    for x in range(wfc.state_space_size[0]):
        last = wfc.state_space_size[2] - 1
        wfc.collapse_cell_to_state([x, 0, 0], StructureRotation(empty_space_air, 0))
        wfc.collapse_cell_to_state([x, 0, last], StructureRotation(empty_space_air, 0))

    for z in range(wfc.state_space_size[2]):
        last = wfc.state_space_size[0] - 1
        wfc.collapse_cell_to_state([0, 0, z], StructureRotation(empty_space_air, 0))
        wfc.collapse_cell_to_state([last, 0, z], StructureRotation(empty_space_air, 0))


def collapse_unbuildable_to_air(wfc: WaveFunctionCollapse, buildable: List[List[bool]]):
    """Collapses all cells that are unbuildable to air

    Args:
        wfc (WaveFunctionCollapse): WFC instance
        buildable (List[List[bool]]): 2D boolean array of X by Z which are true iff it is buildable

    Raises:
        ValueError: invalid size of the buildable array
    """
    if wfc.state_space_size[0] - 2 != len(buildable) or wfc.state_space_size[2] - 2 != len(
        buildable[0]
    ):
        raise ValueError(
            "WFC state space size should have a padding of 1 around the buildable area"
        )

    for x in range(len(buildable)):
        for z in range(len(buildable[x])):
            if not buildable[x][z]:
                wfc.collapse_cell_to_state(
                    [x + 1, 0, z + 1], StructureRotation(empty_space_air, 0)
                )
