from __future__ import annotations
from dataclasses import dataclass
from lib.base import *
from lib.attribute import *
from lib.buff import *


Slots = 'Slots'


Attack = 'Attack'
Defense = 'Defense'
Special = 'Special'
Extra = 'Extra'


EntryType = Literal['Attack', 'Defense', 'Special']


def ser_entry_type(val, where: str = '?', optional: bool = False):
    if optional and val is None:
        return None

    if val not in get_args(EntryType):
        raise Exception('%s => must be an EntryType' % where)

    return val


SlotType = Literal['Attack', 'Defense', 'Special', 'Extra']


def ser_slot_type(val, name: str = '?', optional: bool = False):
    if optional and val is None:
        return None

    if val not in get_args(SlotType):
        raise Exception('%s => must be a SlotType' % name)

    return val


@dataclass(kw_only=True)
class Entry(Resource):
    '''
    词条
    '''

    # 词条类型
    type: EntryType

    # 词条的叠加上限 攻击7 生命3 之类的
    max_piece: int

    # 同一词条叠加带来的提升 List长度必须等于max_piece
    piece_values: Mapping[Attribute | ResID, AttributesList | BuffsList] = {}

    # 「+」值堆叠带来的提升 List长度必须等于max_piece*2
    plus_values: Mapping[Attribute, AttributesList] = {}

    # 展示用的名字
    name: str

    # 稀有度等级
    rare: RareLevel

    # 图标
    icon: str

    @staticmethod
    def find(res_id: str, where: str = '?') -> Entry:
        return Resource.find(res_id, Entry, where)

    @clean()
    def serialize(self) -> dict[str, Any]:
        return {
            **super().serialize(),
            'type': ser_entry_type(self.type, self.here('type')),
            'max_piece': ser_int(self.max_piece, min=0, max=99, where=self.here('max_piece')),
            **self._ser_piece_values(),
            **self._ser_plus_values(),
            'name': ser_str(self.name, self.here('name')),
            'rare': ser_rare_level(self.rare, self.here('rare')),
            'icon': ser_str(self.icon, self.here('icon')),
        }

    @clean()
    def _ser_piece_values(self):
        if not isinstance(self.piece_values, Mapping):
            raise Exception('%s => must be a Mapping' % self.here('piece_values'))

        attributes = {}
        buffs = {}

        for key, list in self.piece_values.items():
            if is_attribute(key):
                attributes[key] = ser_attributes_list(
                    list, self.max_piece, self.here('piece_values.(value)'))
            elif Resource.is_id(key, Buff):
                buffs[key] = ser_buffs_list(
                    list, self.max_piece, self.here('piece_values.(value)'))
            else:
                raise Exception('%s => must be an Attribute|BuffID' %
                                self.here('piece_values.(key)'))

        return {
            'attributes': dict_table(attributes, self.max_piece),
            'buffs': dict_table(buffs, self.max_piece),
        }

    def _ser_plus_values(self):
        if not isinstance(self.plus_values, Mapping):
            raise Exception(self.here('plus_values')+': must be a Mapping')

        attributes = {}

        for key, list in self.plus_values.items():
            if is_attribute(key):
                attributes[key] = ser_attributes_list(
                    list, self.max_piece, self.here('plus_values.(value)'))
            else:
                raise Exception('%s => must be an Attribute' %
                                self.here('plus_values.(key)'))

        return {
            'attributes': dict_table(attributes, self.max_piece * 2),
        }


# 宝石镶嵌列表 [[SlotType, ...], ...]
SlotsList = Sequence[Sequence[SlotType]]


def ser_slots_list(list, size: int, where: str = '?', optional: bool = False):
    if optional and list is None:
        return None

    if not isinstance(list, Sequence):
        raise Exception('%s => must be a SlotsList' % where)

    if len(list) != size:
        raise Exception('%s => size must equal to %d' % (where, size))

    for line in list:
        if not isinstance(line, Sequence):
            raise Exception('%s.(item) => must be a Sequence' % where)

        for item in line:
            ser_slot_type(item, where+'.(item).(item)')

    return list_table(list)


# 词条列表 [[词条piece, 词条plus], ...]
EntriesList = Sequence[Sequence[int, int]]


def ser_entries_list(list, size: int, where: str):
    if not isinstance(list, Sequence):
        raise Exception('%s => must be an EntriesList' % where)

    if len(list) != size:
        raise Exception('%s => size must equal to %d' % (where, size))

    for line in list:
        if not isinstance(line, Sequence):
            raise Exception('%s.(item) => must be a Sequence' % where)

        for item in line:
            ser_rangei(item, min=0, max=99, where=where+'.(item).(item)')

    return list
