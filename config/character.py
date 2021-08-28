from dataclasses import dataclass
from typing import *
from basic import *


@dataclass
class Physics(Serializer):
    shape: Shape
    position: Optional[Transform]


@dataclass
class Properties(Serializer):
    max_health: tuple[float, ...]
    max_shield: tuple[float, ...]
    shield_speed: tuple[float, ...]

    phy_attack: tuple[float, ...]
    elm_attack: tuple[float, ...]
    spe_attack: tuple[float, ...]

    phy_defense: tuple[float, ...]
    elm_defense: tuple[float, ...]
    spe_defense: tuple[float, ...]

    crit_chance_ratio: tuple[float, ...]
    crit_damage_ratio: tuple[float, ...]


@dataclass
class Character(Serializer):
    res_id: str
    min_level: int
    max_level: int
    physics: Physics
    properties: Properties
    type: Literal["Character"] = "Character"
