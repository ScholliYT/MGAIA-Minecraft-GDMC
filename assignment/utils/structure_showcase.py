from typing import List

from gdpc import Block, Editor, Transform
from gdpc import geometry as geo
from glm import ivec3
from tqdm import tqdm

from assignment.utils.structure import Structure, build_structure


def build_structure_showcase(
    editor: Editor, structures: List[Structure], space_between_structures=3
):
    # same for all strucures
    structure_size = structures[0].size

    print("Cleaning up area with air blocks")
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

    print("Placing all structures in all 4 rotations")
    for rotation in tqdm(range(4), desc="Rotation"):
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
