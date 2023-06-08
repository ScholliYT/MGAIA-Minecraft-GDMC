from gdpc import Editor, Transform
from glm import ivec3

from assignment.church.structures import (
    church_altar,
    churchcorner_altar_left,
    churchcorner_altar_right,
    churchcorner_straight,
    churchentrance,
    churchstraight_no_altar,
    churchstraight_to_altar,
)
from assignment.utils.structure import load_structure
from assignment.utils.structure_showcase import build_structure_showcase


def main():
    ED = Editor(buffering=True)

    try:
        ED.transform @= Transform(translation=ivec3(40, 0, 100))

        structures = [
            load_structure(church_altar),
            load_structure(churchcorner_altar_left),
            load_structure(churchcorner_altar_right),
            load_structure(churchcorner_straight),
            load_structure(churchentrance),
            load_structure(churchstraight_no_altar),
            load_structure(churchstraight_to_altar),
        ]

        print("Building church structure showcase")
        build_structure_showcase(editor=ED, structures=structures)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
