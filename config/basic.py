from dataclasses import dataclass
from typing import *
from abc import ABC
from decimal import *


def clamp(x: float, a: float, b: float):
    return max(a, min(x, b))


@dataclass
class Transform:
    rotation: Optional[tuple[float, float, float]] = None
    translation: Optional[tuple[float, float, float]] = None


@dataclass
class Ball:
    radius: float
    rotation: Optional[tuple[float, float, float]] = None
    translation: Optional[tuple[float, float, float]] = None


@dataclass
class Cuboid:
    x: float
    y: float
    z: float
    rotation: Optional[tuple[float, float, float]] = None
    translation: Optional[tuple[float, float, float]] = None


@dataclass
class Capsule:
    half_height: float
    radius: float
    rotation: Optional[tuple[float, float, float]] = None
    translation: Optional[tuple[float, float, float]] = None


@dataclass
class Cone:
    half_height: float
    radius: float
    rotation: Optional[tuple[float, float, float]] = None
    translation: Optional[tuple[float, float, float]] = None


@dataclass
class Cylinder:
    half_height: float
    radius: float
    rotation: Optional[tuple[float, float, float]] = None
    translation: Optional[tuple[float, float, float]] = None


@dataclass
class Plane:
    nx: float
    ny: float
    nz: float
    rotation: Optional[tuple[float, float, float]] = None
    translation: Optional[tuple[float, float, float]] = None


@dataclass
class TriMesh:
    file: str
    name: str
    rotation: Optional[tuple[float, float, float]] = None
    translation: Optional[tuple[float, float, float]] = None


Shape = Union[Ball, Cuboid, Capsule, Cone, Cylinder, Plane, TriMesh]
