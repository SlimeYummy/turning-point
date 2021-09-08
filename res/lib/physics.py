from dataclasses import dataclass
from typing import ClassVar
from lib.basic import Resource, Serializer


@dataclass
class Transform(Resource):
    translation: tuple[float, float, float] | None = None
    rotation: tuple[float, float, float] | None = None


@dataclass
class Shape(Serializer):
    def __init__(self) -> None:
        raise Exception("Shape is an abstract class")


@dataclass
class Ball(Shape):
    type: ClassVar[str] = "Ball"
    radius: float
    translation: tuple[float, float, float] | None = None
    rotation: tuple[float, float, float] | None = None


@dataclass
class Cuboid(Shape):
    type: ClassVar[str] = "Cuboid"
    x: float
    y: float
    z: float
    translation: tuple[float, float, float] | None = None
    rotation: tuple[float, float, float] | None = None


@dataclass
class Capsule(Shape):
    type: ClassVar[str] = "Capsule"
    half_height: float
    radius: float
    translation: tuple[float, float, float] | None = None
    rotation: tuple[float, float, float] | None = None


@dataclass
class Cone(Shape):
    type: ClassVar[str] = "Cone"
    half_height: float
    radius: float
    translation: tuple[float, float, float] | None = None
    rotation: tuple[float, float, float] | None = None


@dataclass
class Cylinder(Shape):
    type: ClassVar[str] = "Cylinder"
    half_height: float
    radius: float
    translation: tuple[float, float, float] | None = None
    rotation: tuple[float, float, float] | None = None


@dataclass
class Plane(Shape):
    type: ClassVar[str] = "Plane"
    nx: float
    ny: float
    nz: float
    translation: tuple[float, float, float] | None = None
    rotation: tuple[float, float, float] | None = None


@dataclass
class TriMesh(Shape):
    type: ClassVar[str] = "TriMesh"
    file: str
    name: str
    translation: tuple[float, float, float] | None = None
    rotation: tuple[float, float, float] | None = None
