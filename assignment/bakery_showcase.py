from typing import List

from gdpc import Block, Editor, Transform
from gdpc import geometry as geo
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
from assignment.utils.structure import Structure, build_structure, load_structure


def build_structure_showcase(
    editor: Editor, structures: List[Structure], space_between_structures=3
):
    # same for all strucures
    structure_size = structures[0].size

    geo.placeCuboid(
        editor,
        ivec3(0, 0, 0),
        ivec3(
            4 * (structure_size.x + 2 * space_between_structures),
            16,
            len(structures) * (structure_size.z + space_between_structures),
        ),
        Block("air"),
    )

    editor.flushBuffer()

    for rotation in range(4):
        with editor.pushTransform(
            Transform(
                translation=ivec3(
                    rotation * (structure_size.x + 2 * space_between_structures), 0, 0
                )
            )
        ):
            for structure_idx, structure in enumerate(structures):
                with editor.pushTransform(
                    Transform(
                        translation=ivec3(
                            0, 0, structure_idx * (structure_size.z + space_between_structures)
                        )
                    )
                ):
                    build_structure(editor, structure, rotation)

    editor.flushBuffer()


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
