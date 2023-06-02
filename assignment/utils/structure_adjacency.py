import logging
from dataclasses import dataclass, field
from typing import Dict, List, Set

from assignment.utils.structure_rotation import StructureRotation

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StructureAdjacency:
    """Store all possible other Structures that can be placed next to this structure

    Assumes that this structure is rotated by 0
    """

    structure_name: str
    empty_space_air: str

    # store a list of structures that can be adjacent in the specified rotation and placed above this
    # (structure_name, rotation)
    y_plus: List[StructureRotation] = field(default_factory=list)
    y_minus: List[StructureRotation] = field(default_factory=list)

    x_plus: List[StructureRotation] = field(default_factory=list)
    x_minus: List[StructureRotation] = field(default_factory=list)

    z_plus: List[StructureRotation] = field(default_factory=list)
    z_minus: List[StructureRotation] = field(default_factory=list)

    def __post_init__(self):
        # Overwrite x an z axis with air structures on all sides by default.
        # This value is only known at runtime as the size of the air tile
        # depends on the size of the other structures.
        filled_by_default = [self.x_plus, self.x_minus, self.z_plus, self.z_minus]
        not_set_yet = [a for a in filled_by_default if a == []]

        for a in not_set_yet:
            for x in all_rotations(self.empty_space_air):
                a.append(x)

    def adjecent_structrues(self, axis: str, self_rotation: int) -> List[StructureRotation]:
        if axis not in ("y_plus", "y_minus", "x_plus", "x_minus", "z_plus", "z_minus"):
            raise ValueError("Invalid axis " + axis)

        # easy cases since everything will rotate along the y-axis
        match axis:
            case "y_plus":
                return list(map(lambda r: r.rotate(self_rotation), self.y_plus))
            case "y_minus":
                return list(map(lambda r: r.rotate(self_rotation), self.y_minus))

        if self_rotation == 0:
            # default case with no rotations
            return getattr(self, axis)
        elif self_rotation in (1, 2, 3):
            rotation_axes = (self.x_plus, self.z_plus, self.x_minus, self.z_minus)
            match axis:
                case "x_plus":
                    return list(
                        map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 0])
                    )  # self.z_minus for rotation 1
                case "z_plus":
                    return list(
                        map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 1])
                    )  # self.x_plus for rotation 1
                case "x_minus":
                    return list(
                        map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 2])
                    )  # self.z_plus for rotation 1
                case "z_minus":
                    return list(
                        map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 3])
                    )  # self.x_minus for rotation 1
            raise NotImplementedError(f"Axis {axis} should have been handled before")
        else:
            raise ValueError("Rotation must be 0,1,2 or 3")


def all_rotations(structure: str):
    return [StructureRotation(structure, r) for r in range(4)]


def check_symmetry(
    structure_adjecencies: Dict[str, StructureAdjacency], structure_subset: None | Set[str] = None
):
    """Verify that the symmetric coutnerpart for each rule is present

    Args:
        structure_adjecencies (Dict[str, StructureAdjacency]): structures and their adjecency rules

    Raises:
        Exception: if no rule was found
        Exception: if too many rules were found
    """
    self_rotation = 0
    structure_names = structure_adjecencies.keys()
    if structure_subset:
        structure_names = structure_subset.intersection(structure_names)

    for s_name in structure_names:
        adj = structure_adjecencies[s_name]

        for axis in ("y_plus", "y_minus", "x_plus", "x_minus", "z_plus", "z_minus"):
            # for axis in ("y_plus","y_minus"):
            rules: List[StructureRotation] = getattr(adj, axis)

            if structure_subset:
                rules = [r for r in rules if r.structure_name in structure_names]

            for rule in rules:
                if rule.structure_name not in structure_names:
                    raise KeyError(f"'{rule.structure_name}' not found in structure_adjecencies")

                other_adj = structure_adjecencies[rule.structure_name]
                opposite_axis = axis[:2] + ("plus" if axis[2:] == "minus" else "minus")

                other_rules: List[StructureRotation] = other_adj.adjecent_structrues(
                    opposite_axis, rule.rotation
                )

                matching_rules = list(
                    filter(
                        lambda r: r.structure_name == s_name and r.rotation == self_rotation,
                        other_rules,
                    )
                )

                if len(matching_rules) == 0:
                    logger.error(
                        "%s.%s: Symmetric rule for %s not found. Expected to find correctly "
                        + "rotated %s in axis %s of %s. But there are actually: %s",
                        s_name,
                        axis,
                        rule,
                        s_name,
                        opposite_axis,
                        rule.structure_name,
                        other_rules,
                    )
                    raise Exception("Expected rule not found")
                elif len(matching_rules) > 1:
                    logger.error(
                        "%s.%s: Multiple symmetric rules for %s found: %s",
                        s_name,
                        axis,
                        rule,
                        matching_rules,
                    )
                    raise Exception("Found too many rules")
