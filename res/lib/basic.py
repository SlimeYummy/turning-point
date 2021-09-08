from dataclasses import dataclass, is_dataclass
from typing import *


@dataclass
class Serializer:
    def serialize(self: Any) -> Any:
        return Serializer.serialize_any(self)

    @staticmethod
    def serialize_any(obj: Any) -> Any:
        typed_obj = obj
        if isinstance(typed_obj, Serializer):
            json = {}

            typ = getattr(type(obj), "type", "")
            if typ != "":
                json["type"] = typ

            if is_dataclass(obj):
                for key in obj.__dataclass_fields__:
                    value = getattr(obj, key)
                    if value != None and value != "":
                        json[key] = Serializer.serialize_any(value)
            else:
                for key, value in obj.__dict__.items():
                    if value != None and value != "":
                        json[key] = Serializer.serialize_any(value)
            return json

        elif isinstance(obj, tuple) or isinstance(obj, list):
            return [Serializer.serialize_any(value) for value in obj]

        elif isinstance(obj, dict):
            return {
                key: Serializer.serialize_any(value)
                for key, value in obj.items()
            }

        else:
            return obj

    @staticmethod
    def serialize_dict_table(obj: Any) -> Any:
        table = Serializer.serialize_any(obj)
        row = 0
        for val in table.values():
            row = max(row, len(val))
        return {
            "type": "DictTable",
            "row": row,
            "column": len(table),
            "table": table,
        }

    @staticmethod
    def serialize_list_table(obj: Any) -> Any:
        table = Serializer.serialize_any(obj)
        row = 0
        for val in table:
            row = max(row, len(val))
        return {
            "type": "ListTable",
            "row": row,
            "column": len(table),
            "table": table,
        }


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

    def serialize(self: Any) -> Any:
        return Serializer.serialize_dict_table(self)
