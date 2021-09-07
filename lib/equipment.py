from dataclasses import dataclass
from lib.basic import *


@dataclass
class WeaponVariant(Serializer):
    name: str
    level: tuple[int, int]
    materials: tuple[dict[str, int], ...]
    slots: tuple[str, ...] | None = None
    attributes: Attributes | None = None

    def serialize(self: Any) -> Any:
        json = {}
        for key in self.__dataclass_fields__:
            value = getattr(self, key)
            if value != None and value != "":
                if key == "materials":
                    json[key] = Serializer.serialize_list_table(value)
                elif key == "slots":
                    json[key] = Serializer.serialize_list_table(value)
                else:
                    json[key] = Serializer.serialize_any(value)
        return json


@dataclass
class Weapon(Resource):
    type: ClassVar[str] = "Weapon"

    name: str
    variants: tuple[WeaponVariant, ...]

    def __init__(
        self, res_id: str, name: str, variants: tuple[WeaponVariant, ...]
    ) -> None:
        super().__init__(res_id)
        self.name = name
        variants = variants


@dataclass
class Soul(Resource):
    type: ClassVar[str] = "Soul"

    name: str
    materials: tuple[dict[str, int], ...]
    slots: tuple[str, ...] | None
    attributes: Attributes | None

    def __init__(
        self,
        res_id: str,
        name: str,
        materials: tuple[dict[str, int], ...],
        slots: tuple[str, ...] | None = None,
        attributes: Attributes | None = None,
    ) -> None:
        super().__init__(res_id)
        self.name = name
        self.materials = materials
        self.slots = slots
        self.attributes = attributes

