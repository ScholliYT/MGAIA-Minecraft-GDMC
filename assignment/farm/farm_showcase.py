from gdpc import Editor, Transform
from glm import ivec3

from assignment.farm.structures import (
    farm_corner,
    farm_corridor_straight,
    farm_corridor_to_farm,
    farm_corridor_to_left,
    farm_corridor_to_open,
    farm_corridor_to_right,
    farm_entrance,
    farm_middle,
    farm_outside_corner,
    farm_outside_corridor_corner,
    farm_outside_corridor_end,
    farm_outside_corridor_to_left,
    farm_outside_corridor_to_right,
    farm_outside_middle,
    farm_outside_wall,
    farm_wall,
)
from assignment.utils.structure import load_structure
from assignment.utils.structure_showcase import build_structure_showcase


def main():
    ED = Editor(buffering=True)

    try:
        ED.transform @= Transform(translation=ivec3(-150, 0, 50))

        structures = [
            load_structure(farm_outside_corridor_corner),
            load_structure(farm_outside_corner),
            load_structure(farm_outside_corridor_end),
            load_structure(farm_outside_corridor_to_left),
            load_structure(farm_outside_corridor_to_right),
            load_structure(farm_outside_middle),
            load_structure(farm_outside_wall),
            load_structure(farm_corner),
            load_structure(farm_corridor_straight),
            load_structure(farm_corridor_to_farm),
            load_structure(farm_corridor_to_left),
            load_structure(farm_corridor_to_open),
            load_structure(farm_corridor_to_right),
            load_structure(farm_entrance),
            load_structure(farm_middle),
            load_structure(farm_wall),
        ]

        print("Building structure showcase")
        build_structure_showcase(editor=ED, structures=structures)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
