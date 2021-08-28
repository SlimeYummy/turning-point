from abc import ABC
from dataclasses import dataclass, is_dataclass
from typing import *
import orjson


class Serializer(ABC):
    def serialize(self: Any) -> dict[str, Any]:
        dict = {}
        if is_dataclass(self):
            for key in self.__dataclass_fields__:
                value = getattr(self, key)
                if value is not None and value is not "":
                    if isinstance(value, Serializer):
                        dict[key] = value.serialize()
                    else:
                        dict[key] = value
        else:
            for key, value in self.__dict__.items():
                if value is not None and value is not "":
                    if isinstance(value, Serializer):
                        dict[key] = value.serialize()
                    else:
                        dict[key] = value
        return dict

    def toJSON(self) -> bytes:
        return orjson.dumps(self.serialize())


class LevelTable(Serializer):
    def __init__(self, **kargs: tuple[float, ...]) -> None:
        for key, value in kargs.items():
            self.__dict__[key] = value

    def __getattr__(self, key: str) -> tuple[float, ...]:
        return self.__dict__[key]


@dataclass
class Properties:
    max_health: Optional[tuple[float, ...]] = None
    health_cure_ratio: Optional[tuple[float, ...]] = None

    attack: Optional[tuple[float, ...]] = None
    attack_up: Optional[tuple[float, ...]] = None
    phy_attack: Optional[tuple[float, ...]] = None
    phy_attack_up: Optional[tuple[float, ...]] = None
    elm_attack: Optional[tuple[float, ...]] = None
    elm_attack_up: Optional[tuple[float, ...]] = None
    spe_attack: Optional[tuple[float, ...]] = None
    spe_attack_up: Optional[tuple[float, ...]] = None

    defense: Optional[tuple[float, ...]] = None
    defense_up: Optional[tuple[float, ...]] = None
    phy_defense: Optional[tuple[float, ...]] = None
    phy_defense_up: Optional[tuple[float, ...]] = None
    elm_defense: Optional[tuple[float, ...]] = None
    elm_defense_up: Optional[tuple[float, ...]] = None
    spe_defense: Optional[tuple[float, ...]] = None
    spe_defense_up: Optional[tuple[float, ...]] = None

    crit_chance_ratio: Optional[tuple[float, ...]] = None
    crit_damage_ratio: Optional[tuple[float, ...]] = None

    max_shield: Optional[tuple[float, ...]] = None
    shield_speed: Optional[tuple[float, ...]] = None

    phy_break_up: Optional[tuple[float, ...]] = None
    elm_break_up: Optional[tuple[float, ...]] = None
    spe_break_up: Optional[tuple[float, ...]] = None


@dataclass
class Transform(Serializer):
    translation: Optional[tuple[float, float, float]] = None
    rotation: Optional[tuple[float, float, float]] = None


@dataclass
class Ball(Serializer):
    radius: float
    translation: Optional[tuple[float, float, float]] = None
    rotation: Optional[tuple[float, float, float]] = None
    type: Literal["Ball"] = "Ball"


@dataclass
class Cuboid(Serializer):
    x: float
    y: float
    z: float
    translation: Optional[tuple[float, float, float]] = None
    rotation: Optional[tuple[float, float, float]] = None
    type: Literal["Cuboid"] = "Cuboid"


@dataclass
class Capsule(Serializer):
    half_height: float
    radius: float
    translation: Optional[tuple[float, float, float]] = None
    rotation: Optional[tuple[float, float, float]] = None
    type: Literal["Capsule"] = "Capsule"


@dataclass
class Cone(Serializer):
    half_height: float
    radius: float
    translation: Optional[tuple[float, float, float]] = None
    rotation: Optional[tuple[float, float, float]] = None
    type: Literal["Cone"] = "Cone"


@dataclass
class Cylinder(Serializer):
    half_height: float
    radius: float
    translation: Optional[tuple[float, float, float]] = None
    rotation: Optional[tuple[float, float, float]] = None
    type: Literal["Cylinder"] = "Cylinder"


@dataclass
class Plane(Serializer):
    nx: float
    ny: float
    nz: float
    translation: Optional[tuple[float, float, float]] = None
    rotation: Optional[tuple[float, float, float]] = None
    type: Literal["Plane"] = "Plane"


@dataclass
class TriMesh(Serializer):
    file: str
    name: str
    translation: Optional[tuple[float, float, float]] = None
    rotation: Optional[tuple[float, float, float]] = None
    type: Literal["TriMesh"] = "TriMesh"


Shape = Union[Ball, Cuboid, Capsule, Cone, Cylinder, Plane, TriMesh]
