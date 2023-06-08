from gdpc import Editor, Transform
from glm import ivec3

from assignment.school.structures import (
    school_cafeteria,
    school_classroom,
    school_corner,
    school_entrance,
    school_library,
    school_lower_stairs,
    school_roof,
    school_upper_entrance,
    school_upper_middle,
    school_upper_stairs
)
from assignment.utils.structure import load_structure
from assignment.utils.structure_showcase import build_structure_showcase


def main():
    ED = Editor(buffering=True)

    try:
        ED.transform @= Transform(translation=ivec3(-100, 0, -200))

        structures = [
            load_structure(school_cafeteria),
            load_structure(school_classroom),
            load_structure(school_corner),
            load_structure(school_entrance),
            load_structure(school_library),
            load_structure(school_lower_stairs),
            load_structure(school_roof),
            load_structure(school_upper_entrance),
            load_structure(school_upper_middle),
            load_structure(school_upper_stairs)
        ]

        print("Building school structure showcase")
        build_structure_showcase(editor=ED, structures=structures)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
