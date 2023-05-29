from gdpc import Editor, Transform
from glm import ivec3

from assignment.bakery.structures import (
    bakery_corner_narrow_to_narrow,
    bakery_corner_narrow_to_wide,
    bakery_corner_wide_to_narrow,
    bakery_corner_wide_to_wide,
    bakery_corridor_corner,
    bakery_corridor_end,
    bakery_corridor_entrance,
    bakery_corridor_straight,
    bakery_corridor_to_left,
    bakery_corridor_to_open,
    bakery_corridor_to_right,
    bakery_entrance_open,
    bakery_inner_corner_narrow,
    bakery_inner_corner_wide,
    bakery_middle_chairs,
    bakery_middle_counter,
    bakery_oven_narrow,
    bakery_oven_wide,
    bakery_wall_counter,
    bakery_wall_narrow,
    bakery_wall_wide,
)
from assignment.utils.structure import load_structure
from assignment.utils.structure_showcase import build_structure_showcase


def main():
    ED = Editor(buffering=True)

    try:
        ED.transform @= Transform(translation=ivec3(50, 0, 50))

        structures = [
            load_structure(bakery_corner_narrow_to_narrow),
            load_structure(bakery_corner_narrow_to_wide),
            load_structure(bakery_corner_wide_to_narrow),
            load_structure(bakery_corner_wide_to_wide),
            load_structure(bakery_corridor_corner),
            load_structure(bakery_corridor_end),
            load_structure(bakery_corridor_entrance),
            load_structure(bakery_corridor_straight),
            load_structure(bakery_corridor_to_left),
            load_structure(bakery_corridor_to_open),
            load_structure(bakery_corridor_to_right),
            load_structure(bakery_entrance_open),
            load_structure(bakery_inner_corner_wide),
            load_structure(bakery_inner_corner_narrow),
            load_structure(bakery_middle_chairs),
            load_structure(bakery_middle_counter),
            load_structure(bakery_oven_narrow),
            load_structure(bakery_oven_wide),
            load_structure(bakery_wall_counter),
            load_structure(bakery_wall_narrow),
            load_structure(bakery_wall_wide),
        ]

        print("Building structure showcase")
        build_structure_showcase(editor=ED, structures=structures)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
