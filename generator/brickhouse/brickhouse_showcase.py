from gdpc import Editor, Transform
from glm import ivec3

from generator.brickhouse.structures import (
    brickhouse_balcony,
    brickhouse_big_window_flat_roof,
    brickhouse_center,
    brickhouse_corner,
    brickhouse_courtyard,
    brickhouse_entrance,
    brickhouse_entrance_stairs,
    brickhouse_inner_corner_m2m,
    brickhouse_middle,
    brickhouse_roofhouse_center,
    brickhouse_roofhouse_corner,
    brickhouse_roofhouse_corner_stairs,
    brickhouse_roofhouse_courtyard,
    brickhouse_roofhouse_inner_corner_m2m,
    brickhouse_roofhouse_middle,
    brickhouse_roofhouse_middle_to_flat,
    brickhouse_roofhouse_middle_to_flat_mirrored_x,
    brickhouse_small_window_flat_roof,
)
from generator.utils.structure import load_structure
from generator.utils.structure_showcase import build_structure_showcase


def main():
    ED = Editor(buffering=True)

    try:
        ED.transform @= Transform(translation=ivec3(0, 0, 100))

        structures = [
            load_structure(brickhouse_entrance),
            load_structure(brickhouse_entrance_stairs),
            load_structure(brickhouse_middle),
            load_structure(brickhouse_balcony),
            load_structure(brickhouse_corner),
            load_structure(brickhouse_courtyard),
            load_structure(brickhouse_inner_corner_m2m),
            load_structure(brickhouse_roofhouse_corner),
            load_structure(brickhouse_roofhouse_corner_stairs),
            load_structure(brickhouse_roofhouse_middle),
            load_structure(brickhouse_roofhouse_middle_to_flat),
            load_structure(brickhouse_roofhouse_middle_to_flat_mirrored_x),
            load_structure(brickhouse_roofhouse_inner_corner_m2m),
            load_structure(brickhouse_roofhouse_courtyard),
            load_structure(brickhouse_center),
            load_structure(brickhouse_roofhouse_center),
            load_structure(brickhouse_small_window_flat_roof),
            load_structure(brickhouse_big_window_flat_roof),
        ]

        print("Building structure showcase")
        build_structure_showcase(editor=ED, structures=structures)

        print("Done!")

    except KeyboardInterrupt:  # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == "__main__":
    main()
