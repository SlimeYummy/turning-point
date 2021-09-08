from dataclasses import dataclass
from lib.basic import *
from lib.physics import *


@dataclass
class RoleVariant(Serializer):
    name: str

    # physics
    shape: Shape
    position: Transform | None

    # value
    attributes: Attributes
    weapons: tuple[str]
    souls: tuple[str]

    def __init__(
        self,
        *,
        name: str,
        shape: Shape,
        position: Transform | None = None,
        attributes: Attributes,
        weapons: tuple[str],
        souls: tuple[str],
    ) -> None:
        super().__init__()
        self.name = name
        self.shape = shape
        self.position = position
        self.attributes = attributes
        self.weapons = weapons
        self.souls = souls


@dataclass
class Role(Resource):
    type: ClassVar[str] = "Role"

    name: str
    level: tuple[int, int]
    variants: tuple[RoleVariant, ...]

    def __init__(
        self,
        res_id: str,
        *,
        name: str,
        level: tuple[int, int],
        variants: tuple[RoleVariant, ...],
    ) -> None:
        super().__init__(res_id)
        self.name = name
        self.level = level
        self.variants = variants


@dataclass
class Enemy(Resource):
    type: ClassVar[str] = "Enemy"

    name: str
    level: int
    shape: Shape
    position: Transform | None
    attributes: Attributes

    def __init__(
        self,
        res_id: str,
        *,
        name: str,
        level: int,
        shape: Shape,
        position: Transform | None,
        attributes: Attributes,
    ) -> None:
        super().__init__(res_id)
        self.name = name
        self.level = level
        self.shape = shape
        self.position = position
        self.attributes = attributes
