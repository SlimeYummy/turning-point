from typing import *
from lib.base import *


MaxHealth = 'MaxHealth'
MaxHealthUp = 'MaxHealthUp'
MaxHealthDown = 'MaxHealthDown'

HealthCure = 'HealthCure'
HealthCureUp = 'HealthCureUp'
HealthCureDown = 'HealthCureDown'

MaxStamina = 'MaxStamina'
MaxStaminaUp = 'MaxStaminaUp'
MaxStaminaDown = 'MaxStaminaDown'
ExtraStamina = 'ExtraStamina'

StaminaRecovery = 'StaminaRecovery'
StaminaRecoveryUp = 'StaminaRecoveryUp'
StaminaRecoveryDown = 'StaminaRecoveryDown'

Damage = 'Damage'

Attack = 'Attack'
AttackUp = 'AttackUp'
AttackDown = 'AttackDown'

Defense = 'Defense'
DefenseUp = 'DefenseUp'
DefenseDown = 'DefenseDown'

CriticalChance = 'CriticalChance'
CriticalDamage = 'CriticalDamage'

BonusUp = 'BonusUp'
BonusDown = 'BonusDown'
PhysicalBonusUp = 'PhysicalBonusUp'
PhysicalBonusDown = 'PhysicalBonusDown'
ElementalBonusUp = 'ElementalBonusUp'
ElementalBonusDown = 'ElementalBonusDown'
MagicalBonusUp = 'MagicalBonusUp'
MagicalBonusDown = 'MagicalBonusDown'
CutBonusUp = 'CutBonusUp'
CutBonusDown = 'CutBonusDown'
BluntBonusUp = 'BluntBonusUp'
BluntBonusDown = 'BluntBonusDown'
AmmoBonusUp = 'AmmoBonusUp'
AmmoBonusDown = 'AmmoBonusDown'
FireBonusUp = 'FireBonusUp'
FireBonusDown = 'FireBonusDown'
IceBonusUp = 'IceBonusUp'
IceBonusDown = 'IceBonusDown'
ThunderBonusUp = 'ThunderBonusUp'
ThunderBonusDown = 'ThunderBonusDown'

Resistance = 'Resistance'
ResistancePass = 'ResistancePass'
PhysicalResistance = 'PhysicalResistance'
PhysicalResistancePass = 'PhysicalResistancePass'
ElementalResistance = 'ElementalResistance'
ElementalResistancePass = 'ElementalResistancePass'
MagicalResistance = 'MagicalResistance'
MagicalResistancePass = 'MagicalResistancePass'
CutResistance = 'CutResistance'
CutResistancePass = 'CutResistancePass'
BluntResistance = 'BluntResistance'
BluntResistancePass = 'BluntResistancePass'
AmmoResistance = 'AmmoResistance'
AmmoResistancePass = 'AmmoResistancePass'
FireResistance = 'FireResistance'
FireResistancePass = 'FireResistancePass'
IceResistance = 'IceResistance'
IceResistancePass = 'IceResistancePass'
ThunderResistance = 'ThunderResistance'
ThunderResistancePass = 'ThunderResistancePass'

GuardShield = 'GuardShield'
GuardShieldPass = 'GuardShieldPass'
BlockShield = 'BlockShield'
BlockShieldPass = 'BlockShieldPass'
DodgeShield = 'DodgeShield'
DodgeShieldPass = 'DodgeShieldPass'
EndureShield = 'EndureShield'
EndureShieldPass = 'EndureShieldPass'

Break = 'Break'
BreakUp = 'BreakUp'
BreakDown = 'BreakDown'

Attribute = Literal[
    'MaxHealth',
    'MaxHealthUp',
    'MaxHealthDown',

    'HealthCure',
    'HealthCureUp',
    'HealthCureDown',

    'MaxStamina',
    'MaxStaminaUp',
    'MaxStaminaDown',
    'ExtraStamina',

    'StaminaRecovery',
    'StaminaRecoveryUp',
    'StaminaRecoveryDown',

    'Damage',

    'Attack',
    'AttackUp',
    'AttackDown',

    'Defense',
    'DefenseUp',
    'DefenseDown',

    'CriticalChance',
    'CriticalDamage',

    'BonusUp',
    'BonusDown',
    'PhysicalBonusUp',
    'PhysicalBonusDown',
    'ElementalBonusUp',
    'ElementalBonusDown',
    'MagicalBonusUp',
    'MagicalBonusDown',
    'CutBonusUp',
    'CutBonusDown',
    'BluntBonusUp',
    'BluntBonusDown',
    'AmmoBonusUp',
    'AmmoBonusDown',
    'FireBonusUp',
    'FireBonusDown',
    'IceBonusUp',
    'IceBonusDown',
    'ThunderBonusUp',
    'ThunderBonusDown',

    'Resistance',
    'ResistancePass',
    'PhysicalResistance',
    'PhysicalResistancePass',
    'ElementalResistance',
    'ElementalResistancePass',
    'MagicalResistance',
    'MagicalResistancePass',
    'CutResistance',
    'CutResistancePass',
    'BluntResistance',
    'BluntResistancePass',
    'AmmoResistance',
    'AmmoResistancePass',
    'FireResistance',
    'FireResistancePass',
    'IceResistance',
    'IceResistancePass',
    'ThunderResistance',
    'ThunderResistancePass',

    'GuardShield',
    'GuardShieldPass',
    'BlockShield',
    'BlockShieldPass',
    'DodgeShield',
    'DodgeShieldPass',
    'EndureShield',
    'EndureShieldPass',

    'Break',
    'BreakUp',
    'BreakDown',
]

_AttributesDict_ = {k: True for k in get_args(Attribute)}


def ser_attribute(val, where: str = '?', optional: bool = False):
    if optional and val is None:
        return None

    if val not in _AttributesDict_:
        raise Exception('%s => must be an Attribute' % where)
    return val


def is_attribute(val):
    return val in _AttributesDict_


# 属性列表 [属性值, ...]
AttributesList = Sequence[float]


def ser_attributes_list(
    list,
    size: int,
    where: str = '?',
    optional: bool = False,
    min: number | None = None,
    max: number | None = None,
):
    if optional and list is None:
        return None

    if not isinstance(list, Sequence):
        raise Exception('%s => must be an AttributesList' % where)

    if len(list) != size:
        raise Exception('%s => size must equal to %d' % (where, size))

    for attr in list:
        ser_num(attr, where+'.(item)', min, max)

    return list
