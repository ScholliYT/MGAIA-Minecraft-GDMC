from typing import List

from gdpc import Block, Editor, Transform
from gdpc import geometry as geo
from glm import ivec3

from assignment.farm.structures import (
    farm_outside_corner,
    farm_outside_corridor_corner,
    farm_outside_corridor_end,
    farm_outside_corridor_to_left,
    farm_outside_corridor_to_right,
    farm_outside_middle,
    farm_outside_wall,
    farm_corner,
    farm_corridor_straight,
    farm_corridor_to_farm,
    farm_corridor_to_left,
    farm_corridor_to_open,
    farm_corridor_to_right,
    farm_entrance,
    farm_middle,
    farm_wall,
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
