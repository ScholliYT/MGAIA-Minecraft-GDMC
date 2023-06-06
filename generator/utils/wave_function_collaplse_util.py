from typing import List

from generator.utils.structure_rotation import StructureRotation
from generator.utils.wave_function_collapse import WaveFunctionCollapse


def print_state(wfc: WaveFunctionCollapse, air_name: str | None = None):
    for y in range(wfc.state_space_size[1]):
        print("Layer y=" + str(y))
        for x in reversed(range(wfc.state_space_size[0])):
            for z in range(wfc.state_space_size[2]):
                state = wfc.state_space[x][y][z]
                if (
                    air_name is not None
                    and len(state) == 1
                    and (list(state)[0].structure_name == air_name)
                ):
                    print("  ", end=",")
                else:
                    print("{:02d}".format(len(state)), end=",")
            print()
        print()


def collapse_to_air_on_outer_rectangle(wfc: WaveFunctionCollapse, empty_space_air: str):
    for x in range(wfc.state_space_size[0]):
        last = wfc.state_space_size[2] - 1
        wfc.collapse_cell_to_state([x, 0, 0], StructureRotation(empty_space_air, 0))
        wfc.collapse_cell_to_state([x, 0, last], StructureRotation(empty_space_air, 0))

    for z in range(wfc.state_space_size[2]):
        last = wfc.state_space_size[0] - 1
        wfc.collapse_cell_to_state([0, 0, z], StructureRotation(empty_space_air, 0))
        wfc.collapse_cell_to_state([last, 0, z], StructureRotation(empty_space_air, 0))


def collapse_unbuildable_to_air(
    wfc: WaveFunctionCollapse, buildable: List[List[bool]], empty_space_air: str
):
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
