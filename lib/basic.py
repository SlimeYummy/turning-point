from dataclasses import dataclass, is_dataclass
from typing import *
import json


class Resource:
    type: str | None = None

    def serialize(self) -> Any:
        dict = {}

        typ = type(self).type
        if typ != None and typ != "":
            dict["type"] = typ

        if is_dataclass(self):
            for key in self.__dataclass_fields__:
                value = getattr(self, key)
                if value != None and value != "":
                    if isinstance(value, Resource):
                        dict[key] = value.serialize()
                    else:
                        dict[key] = value
        else:
            for key, value in self.__dict__.items():
                if value != None and value != "":
                    if isinstance(value, Resource):
                        dict[key] = value.serialize()
                    else:
                        dict[key] = value
        return dict

    def toJSON(self) -> str:
        return json.dumps(self.serialize())


class LevelTable(Resource):
    def __init__(self, **kwargs: tuple[float, ...]) -> None:
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __getattr__(self, key: str) -> tuple[float, ...]:
        return self.__dict__[key]


@dataclass
class Properties(Resource):
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
