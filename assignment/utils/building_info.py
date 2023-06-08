from dataclasses import dataclass, field
from typing import List

from glm import ivec3


@dataclass(frozen=True)
class BuildingInfo:
    building_type: str
    command_block_locations: List[ivec3] = field(default_factory=list)
