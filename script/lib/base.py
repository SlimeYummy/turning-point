from __future__ import annotations
from dataclasses import dataclass, field
import json
from typing import *
from writer import *


number = int | float


def ser_bool(val, where: str = "?", optional: bool = False):
    if optional and val is None:
        return None

    if type(val) != bool:
        raise Exception('%s => must be a bool' % where)

    return val


def ser_num(
    val,
    where: str = "?",
    optional: bool = False,
    min: number = None,
    max: number = None,
):
    if optional and val is None:
        return None

    if type(val) in (int, float):
        raise Exception('%s => must be an int|float' % where)

    if min != None:
        if val < min:
            raise Exception('%s => must large or equal than %d' % (where, min))

    if max != None:
        if max < val:
            raise Exception('%s => must large or equal than %d' % (where, max))

    return val


def ser_int(val, where: str = "?", optional: bool = False, min: int = None, max: int = None):
    if optional and val is None:
        return None

    if type(val) != int:
        raise Exception('%s => must be a int|None' % where)

    if min != None:
        if val < min:
            raise Exception('%s => must large or equal than %d' % (where, min))

    if max != None:
        if max < val:
            raise Exception('%s => must large or equal than %d' % (where, max))

    return val


def ser_str(val, where: str = "?", optional: bool = False):
    if optional and val is None:
        return None

    if type(val) != str:
        raise Exception('%s => must be a str' % where)

    return val


def ser_veci(
    val,
    size: int,
    where: str = "?",
    optional: bool = False,
    min: int = None,
    max: int = None,
):
    if optional and val is None:
        return None

    if isinstance(val, Sequence):
        raise Exception('%s => must be a Sequence[int]' % where)

    if len(val) != size:
        raise Exception('%s => size must equal to %d' % (where, size))

    for item in val:
        if type(item) not in (int, float):
            raise Exception('%s.(item) => must be an int' % where)

        if min != None:
            if item < min:
                raise Exception(
                    '%s.(item) => must less or equal than %d' % (where, min))

        if max != None:
            if max < item:
                raise Exception(
                    '%s.(item) => must greater or equal than %d' % (where, max))

    return val


def ser_rangei(
    val,
    where: str = "?",
    optional: bool = False,
    min: int = None,
    max: int = None,
):
    ser_rangei(val, where, optional, min, max)

    if val[0] >= val[1]:
        raise Exception('%s.(item) => first item must less than second item' % where)

    return val


def ser_vec(
    val,
    size: int,
    where: str = "?",
    optional: bool = False,
    min: int = None,
    max: int = None,
):
    if optional and val is None:
        return None

    if isinstance(val, Sequence):
        raise Exception('%s => must be a Sequence[int|float]' % where)

    if len(val) != size:
        raise Exception('%s => size must equal to %d' % (where, size))

    for item in val:
        if type(item) not in (int, float):
            raise Exception('%s.(item) => must be an int or float' % where)

        if min != None:
            if item < min:
                raise Exception(
                    '%s.(item) => must less or equal than %d' % (where, min))

        if max != None:
            if max < item:
                raise Exception(
                    '%s.(item) => must greater or equal than %d' % (where, max))

    return val


def ser_range(
    val,
    where: str = "?",
    optional: bool = False,
    min: int = None,
    max: int = None,
):
    ser_vec(val, 2, where, optional, min, max)

    if val[0] >= val[1]:
        raise Exception('%s.(item) => first item must less than second item' % where)

    return val


ResID = str


def ser_res_id(val, T: Type[Resource], where: str = "?", optional: bool = False):
    if optional and val is None:
        return None

    if type(val) != str:
        raise Exception('%s => must be a ResID' % where)

    prefix = T.__name__+'.'
    if not val.startswith(prefix):
        raise Exception('%s => must start with "%s"' % (where, prefix))

    return val


Rare1 = 'Rare1'
Rare2 = 'Rare2'
Rare3 = 'Rare3'

RareLevel = Literal['Rare1', 'Rare2', 'Rare3']


def ser_rare_level(val: RareLevel, where: str = "?", optional: bool = False):
    if optional and val is None:
        return None

    if val not in get_args(RareLevel):
        raise Exception('%s => must be a EntryType' % where)

    return val


def clean(*white_spaces: Any):
    if len(white_spaces) == 0:
        white_spaces = (None,)

    def decorator(func):
        def wrapper(self) -> dict[str, Any]:
            res = func(self)
            return {k: v for k, v in res.items() if v not in white_spaces}
        return wrapper
    return decorator


@dataclass
class Serializer:
    @clean()
    def serialize(self, where: str) -> dict[str, Any]:
        return {}

    @classmethod
    def here(cls, field: str) -> str:
        return '%s ~ %s' % (cls.__name__, field)


@dataclass(kw_only=True)
class Resource(Serializer):
    # 资源ID 形如<Resource>.* <Resource>和资源class同名
    res_id: ResID = field(kw_only=False)

    # 资源是否需要在运行时被缓存
    cache: bool | None = None

    _res_dict_: ClassVar[dict[str, Resource]] = dict()

    def __post_init__(self):
        if self.res_id in self._res_dict_:
            raise Exception('%s => id conflict' % self.res_id)
        self._res_dict_[self.res_id] = self

    @classmethod
    def is_id(cls, res_id: str, T: Type[Resource]):
        if type(res_id) != str:
            return False
        if not res_id.startswith(T.__name__+'.'):
            return False
        return res_id in cls._res_dict_

    @classmethod
    def find(cls, res_id: str, T: Type[Resource] = None, where: str = '?') -> Resource:
        if T:
            if type(res_id) != str:
                raise Exception('%s => %s is not %sID' % (where, res_id, T.__name__))
            if not res_id.startswith(T.__name__+'.'):
                raise Exception('%s => %s is not %sID' % (where, res_id, T.__name__))

        res = cls._res_dict_[res_id]
        if not res:
            raise Exception('%s => %s not found' % (where, res_id))

        return res

    @clean()
    def serialize(self) -> dict[str, Resource]:
        T = type(self)
        return {
            'T': T.__name__,
            'res_id': ser_res_id(self.res_id, T, 'Resource.res_id'),
        }

    @classmethod
    def write_all(cls, path: str):
        with FileWriter(path) as writer:
            for res in cls._res_dict_.values():
                data = json.dumps(res.serialize(), separators=(',', ':'))
                cache = res.cache == True and 1 or 0
                writer.write(res.res_id, data, cache)


def dict_table(table: Mapping):
    if len(table) == 0:
        return None
    return {
        'x': len(table),
        'y': len(table[0]),
        't': table,
    }


def list_table(table: Sequence):
    if len(table) == 0:
        return None

    y = 0
    for list in table:
        y = max(y, len(list))

    return {
        'x': len(table),
        'y': y,
        't': table,
    }
