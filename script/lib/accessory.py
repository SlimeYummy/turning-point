from __future__ import annotations
from dataclasses import dataclass
from lib.base import *
from lib.attribute import *
from lib.entry import *


@dataclass
class RandomAttribute(Serializer):
    # 名称 在RandomAttributes内唯一
    random_id: int

    # 属性名
    attribute: Attribute

    # 属性值列表
    values: AttributesList

    @clean()
    def serialize(self, level: int) -> dict[str, Any]:
        return {
            **super().serialize(),
            'random_id': ser_int(self.random_id, min=0, max=65535, where=self.here('random_id')),
            'attribute': ser_attribute(self.attribute, self.here('attribute')),
            'values': ser_attributes_list(self.values, level, self.here('values')),
        }


@dataclass(kw_only=True)
class RandomAttributes:
    # 值列表
    values: Sequence[RandomAttribute]

    @clean()
    def serialize(self, level: int) -> dict[str, Any]:
        return {
            **super().serialize(),
            'values': self._ser_values(level),
        }

    def _ser_values(self, level: int):
        if not isinstance(self.values, Sequence):
            raise Exception('%s => must be a Sequence' % self.here('values'))

        if len(list) <= 0:
            raise Exception('%s => size must greater than 0' % self.here('values'))

        for v in self.values:
            if not isinstance(v, RandomAttribute):
                raise Exception('%s => must be a RandomAttribute' % self.here('values.(item)'))

        return [v.serialize(level) for v in self.values]

    @staticmethod
    def find(res_id: str, where: str = '?') -> RandomAttributes:
        return Resource.find(res_id, RandomAttributes, where)


@dataclass
class RandomEntry:
    # 名称 在RandomEntries内唯一
    random_id: int

    # Entry的ID
    entry: ResID

    # 属性值列表
    values: EntriesList

    @clean()
    def serialize(self, level: int) -> dict[str, Any]:
        return {
            **super().serialize(),
            'random_id': ser_int(self.random_id, min=0, max=65535, where=self.here('random_id')),
            'entry': ser_res_id(self.attribute, Entry, self.here('entry')),
            'values': ser_entries_list(self.values, level, self.here('values')),
        }


@dataclass(kw_only=True)
class RandomEntries:
    # 值列表
    values: Sequence[RandomEntry]

    @clean()
    def serialize(self, level: int) -> dict[str, Any]:
        return {
            **super().serialize(),
            'values': self._ser_values(level),
        }

    def _ser_values(self, level: int):
        if not isinstance(self.values, Sequence):
            raise Exception('%s => must be a Sequence' % self.here('values'))

        if len(list) <= 0:
            raise Exception('%s => size must greater than 0' % self.here('values'))

        for v in self.values:
            if not isinstance(v, RandomEntry):
                raise Exception('%s => must be a RandomEntry' % self.here('values.(item)'))

        return [v.serialize(level) for v in self.values]

    @staticmethod
    def find(res_id: str, where: str = '?') -> RandomEntries:
        return Resource.find(res_id, RandomEntries, where)


@dataclass(kw_only=True)
class Accessory(Resource):
    '''
    装饰品
    装饰品的属性与词条都是随机生成的
    随机属性由AccessoryAttributes定义
    随机词条由AccessoryEntries定义
    '''

    # 最大等级
    max_level: int

    # 每一级的属性列表
    values: Mapping[
        Attribute | Literal['Slots'] | ResID,
        AttributesList | SlotsList | EntriesList | BuffsList,
    ]

    # 随机属性列表 存储AccessoryAttributes或AccessoryEntries的ID
    random_values: Sequence[ResID]

    # 展示用的名字
    name: str

    # 稀有度等级
    rare: RareLevel

    # 图标
    icon: str

    @staticmethod
    def find(res_id: str, where: str = '?') -> Accessory:
        return Resource.find(res_id, Accessory, where)

    @clean()
    def serialize(self) -> dict[str, Any]:

        return {
            **super().serialize(),
            'max_level': ser_int(self.max_level, min=0, max=99, where=self.here('max_level')),
            **self._ser_values(),
            **self._ser_random_values(),
            'name': ser_str(self.name, self.here('name')),
            'rare': ser_rare_level(self.rare, self.here('rare')),
            'icon': ser_str(self.icon, self.here('icon')),
        }

    @clean(None, {})
    def _ser_values(self):
        if not isinstance(self.values, Mapping):
            raise Exception('%s => must be a Mapping' % self.here('values'))

        attributes = {}
        slots = None
        buffs = {}
        entries = {}

        for key, list in self.values.items():
            if is_attribute(key):
                attributes[key] = ser_attributes_list(
                    list, self.max_level, self.here('values.(value)'))
            elif key == Slots:
                slots = ser_slots_list(list, self.max_level, self.here('values.(value)'))
            elif Resource.is_id(key, Entry):
                entries[key] = ser_entries_list(
                    list, self.max_level, self.here('values.(value)'))
            elif Resource.is_id(key, Buff):
                buffs[key] = ser_buffs_list(
                    list, self.max_level, self.here('values.(value)'))
            else:
                raise Exception('%s => must be an Attribute|"Slots"|Entries|BuffID' %
                                self.here('values.(key)'))

        return {
            'attributes': dict_table(attributes, self.max_level),
            'slots': slots,
            'entries': dict_table(entries, self.max_level),
            'buffs': dict_table(buffs, self.max_level),
        }

    @clean(None, [])
    def _ser_random_values(self):
        if not isinstance(self.values, Sequence):
            raise Exception('%s => must be a Sequence' % self.here('random_values'))

        attributes = []
        entries = []

        for id in self.random_values:
            if Resource.is_id(id, RandomAttribute):
                attributes.append(id)
            elif Resource.is_id(id, RandomEntries):
                entries.append(id)
            else:
                raise Exception('%s => must be a RandomAttributeID|RandomEntriesID' %
                                self.here('random_values.(item)'))
