from dataclasses import dataclass, is_dataclass
from typing import *
import json


class Serializer:
    def serialize(self: Any) -> Any:
        dict = {}

        typ = getattr(type(self), "type", "")
        if typ != "":
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


@dataclass
class Resource(Serializer):
    res_id: str

    def __init__(self, res_id: str) -> None:
        super().__init__()
        self.res_id = res_id


TapAttack = "TapAttack"
HoldAttack = "HoldAttack"
TapAttack1 = "TapAttack1"
HoldAttack1 = "HoldAttack1"
TapAttack2 = "TapAttack2"
HoldAttack2 = "HoldAttack2"
TapDefense = "TapDefense"
HoldDefense = "HoldDefense"
TapSprint = "TapSprint"
TapSkill = "TapSkill"
HoldSkill = "HoldSkill"


KeyInput = Literal[
    "TapAttack",
    "HoldAttack",
    "TapAttack1",
    "HoldAttack1",
    "TapAttack2",
    "HoldAttack2",
    "TapDefense",
    "HoldDefense",
    "TapSprint",
    "TapSkill",
    "HoldSkill",
]


Unrestricted = "Unrestricted"  # 无限制
Actionable1 = "Actionable1"  # 可衔接等级一以上动作
Actionable2 = "Actionable2"  # 可衔接等级二以上动作
Actionable3 = "Actionable3"  # 可衔接等级三以上动作
Derivable = "Derivable"  # 可衔接技能派生
Cancelable = "Cancelable"  # 可强制取消动作
Uncontrolled = "Uncontrolled"  # 不受控

ControlLevel = Literal[
    "Unrestricted",
    "Actionable1",
    "Actionable2",
    "Actionable3",
    "Derivable",
    "Cancelable",
    "Uncontrolled",
]


@dataclass
class Attributes(Serializer):
    max_health: tuple[float, ...] | None = None
    health_cure_ratio: tuple[float, ...] | None = None

    attack: tuple[float, ...] | None = None
    attack_up: tuple[float, ...] | None = None
    phy_attack: tuple[float, ...] | None = None
    phy_attack_up: tuple[float, ...] | None = None
    elm_attack: tuple[float, ...] | None = None
    elm_attack_up: tuple[float, ...] | None = None
    spe_attack: tuple[float, ...] | None = None
    spe_attack_up: tuple[float, ...] | None = None

    defense: tuple[float, ...] | None = None
    defense_up: tuple[float, ...] | None = None
    phy_defense: tuple[float, ...] | None = None
    phy_defense_up: tuple[float, ...] | None = None
    elm_defense: tuple[float, ...] | None = None
    elm_defense_up: tuple[float, ...] | None = None
    spe_defense: tuple[float, ...] | None = None
    spe_defense_up: tuple[float, ...] | None = None

    crit_chance_ratio: tuple[float, ...] | None = None
    crit_damage_ratio: tuple[float, ...] | None = None

    max_shield: tuple[float, ...] | None = None
    shield_speed: tuple[float, ...] | None = None

    phy_break_up: tuple[float, ...] | None = None
    elm_break_up: tuple[float, ...] | None = None
    spe_break_up: tuple[float, ...] | None = None
