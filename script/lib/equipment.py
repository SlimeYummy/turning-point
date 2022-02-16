from __future__ import annotations
from dataclasses import dataclass
from lib.base import *
from lib.attribute import *
from lib.buff import *
from lib.entry import *
from lib.script import *


Equipment1 = 'Equipment1'
Equipment2 = 'Equipment2'
Equipment3 = 'Equipment3'

EquipmentType = Literal['Equipment1', 'Equipment2', 'Equipment3']


def ser_equipment_type(val, where: str = '?', optional: bool = False):
    if optional and list is None:
        return None

    if val not in get_args(EquipmentType):
        raise Exception('%s => must be an EquipmentType' % where)

    return val


@dataclass(kw_only=True)
class Equipment(Resource):
    '''
    武器&装备
    '''

    # 装备类型 决定装备能用于哪个装备槽
    type: EquipmentType

    # 启用条件 控制装备树的逐步开启
    # enable_if: Script

    # 等级范围 [最低等级, 最高等级]
    level: Sequence[int, int]

    # 装备树中的父节点 [装备ID, 等级]
    parents: Mapping[ResID, int]

    # 每一级的武器强化素材列表
    materials: Sequence[Mapping[ResID, int]]

    # 每一级的属性列表
    values: Mapping[
        Attribute | Literal['Slots'] | ResID,
        AttributesList | SlotsList | EntriesList | BuffsList,
    ]

    # 脚本 用于实现特殊功能
    scripts: Sequence[BuildScript | HitScript | HurtScript | TickScript]

    # 展示用的名字
    name: str

    # 稀有度等级
    rare: RareLevel

    # 图标
    icon: str

    # 角标图标
    sub_icon: str

    @staticmethod
    def find(res_id: str, where: str = '?') -> Equipment:
        return Resource.find(res_id, Equipment, where)

    @clean()
    def serialize(self) -> dict[str, Any]:
        return {
            **super().serialize(),
            'type': ser_equipment_type(self.type, self.here('type')),
            # 'enable_if': ser_script(self.type, optional=True, where=self.here('enable_if')),
            'level': ser_rangei(self.level, min=0, max=99, where=self.here('level')),
            'parents': self._ser_parents(),
            'materials': self._ser_materials(),
            **self._ser_values(),
            'name': ser_str(self.name, self.here('name')),
            'rare': ser_rare_level(self.rare, self.here('rare')),
            'icon': ser_str(self.icon, self.here('icon')),
            'sub_icon': ser_str(self.icon, self.here('sub_icon')),
        }

    def _ser_parents(self):
        if not isinstance(self.parents, Mapping):
            raise Exception('%s => must be a Mapping' % self.here('parents'))

        for id, level in self.parents.items():
            parent = Equipment.find(id, self.here('parents.(key)'))

            if parent.type != self.type:
                raise Exception('%s => type must equal to parent' % self.here('parents.(value)'))

            if level < parent.level[0] or parent.level[1] < level:
                raise Exception('%s => level must in parent\'s range' %
                                self.here('parents.(value)'))

        return self.parents

    def _ser_materials(self):
        if not isinstance(self.materials, Sequence):
            raise Exception('%s => must be a Sequence' % self.here('materials'))

        for dict in self.materials:
            if not isinstance(dict, Mapping):
                raise Exception('%s => must be a Mapping' % self.here('materials.(item)'))

            for id, cnt in dict.items():
                Resource.find(id, where='materials.(item).(key)')
                ser_int(cnt, min=0, where='materials.(item).(value)')

        return list_table(self.materials)

    @clean(None, {})
    def _ser_values(self):
        if not isinstance(self.values, Mapping):
            raise Exception('%s => must be a Mapping' % self.here('values'))

        attributes = {}
        slots = None
        buffs = {}
        entries = {}
        level = self.level[1] - self.level[0]

        for key, list in self.values.items():
            if is_attribute(key):
                attributes[key] = ser_attributes_list(
                    list, level, self.here('values.(value)'))
            elif key == Slots:
                slots = ser_slots_list(list, level, self.here('values.(value)'))
            elif Resource.is_id(key, Entry):
                entries[key] = ser_entries_list(
                    list, level, self.here('values.(value)'))
            elif Resource.is_id(key, Buff):
                buffs[key] = ser_buffs_list(
                    list, level, self.here('values.(value)'))
            else:
                raise Exception('%s => must be an Attribute|"Slots"|Entries|BuffID' %
                                self.here('values.(key)'))

        return {
            'attributes': dict_table(attributes, level),
            'slots': slots,
            'entries': dict_table(entries, level),
            'buffs': dict_table(buffs, level),
        }


# @dataclass(kw_only=True)
# class EquipmentX(Serializer):
#     id: str
#     name: str = ''
#     requirements: Sequence[Requirement] = None
#     level: tuple[int, int]
#     materials: Sequence[Mapping[str, int]] = field(
#         default=None, metadata={'table': 1}
#     )
#     attributes: Attributes | None = None
#     slots: Sequence[Sequence[SlotType]] | None = field(
#         default=None, metadata={'table': 1}
#     )
#     buffs: Sequence[Mapping[str, int]] | None = field(
#         default=None, metadata={'table': 1}
#     )

#     def verify(self) -> bool:
#         if not self.id:
#             raise VerifyFailed
#         level = self.level[1] - self.level[0] + 1
#         if level <= 0:
#             raise VerifyFailed
#         self.materials and self.verity_list_table(self.materials, level)
#         self.attributes and self.attributes(level)
#         self.slots and self.verity_list_table(self.slots, level)
#         self.buffs and self.verity_list_table(self.buffs, level)


# @dataclass(kw_only=True)
# class Equipment(Resource):
#     T: str = field(default='Equipment', init=False)

#     name: str = ''
#     variants: Sequence[EquipmentX]

#     def verify(self) -> bool:
#         super().verify()
#         for variant in self.variants:
#             variant.verify()
