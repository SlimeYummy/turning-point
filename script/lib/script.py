from dataclasses import dataclass, field
from lib.base import *


@dataclass
class Script(Serializer):
    def __init__(self) -> None:
        raise Exception('Shape is an abstract class')

    def serialize(self) -> dict[str, Any]:
        return {'T': type(self).__name__}


@dataclass(kw_only=True)
class BuildScript(Script):
    '''
    Env 环境信息等杂项（等级等）
    ValuesIn in 原始的角色数值
    ValuesOut out 修改后的角色数值
    '''

    script: str

    @clean()
    def serialize(self, where: str = '?') -> dict[str, Any]:
        return {
            **super().serialize(),
            'script': ser_str(self.script, where)
        }


@dataclass(kw_only=True)
class HitScript(Script):
    '''
    Env 环境信息等杂项（等级等）
    SourceIn in 原始的攻击发起者属性
    TargetIn in 原始的攻击接受者属性
    Effect in 攻击伤害数据
    SourceOut out 修改后的攻击发起者属性
    TargetOut out 修改后的攻击接受者属性
    '''

    script: str

    @clean()
    def serialize(self, where: str = '?') -> dict[str, Any]:
        return {
            **super().serialize(),
            'script': ser_str(self.script, where)
        }


@dataclass(kw_only=True)
class HurtScript(Script):
    '''
    Env 环境信息等杂项（等级等）
    SourceIn in 原始的攻击发起者属性
    TargetIn in 原始的攻击接受者属性
    Effect in 攻击伤害数据
    SourceOut out 修改后的攻击发起者属性
    TargetOut out 修改后的攻击接受者属性
    '''

    script: str

    @clean()
    def serialize(self, where: str = '?') -> dict[str, Any]:
        return {
            **super().serialize(),
            'script': ser_str(self.script, where)
        }


@dataclass(kw_only=True)
class HealScript(Script):
    '''
    Env 环境信息等杂项（等级等）
    SourceIn in 原始的恢复发起者属性
    TargetIn in 原始的恢复接受者属性
    Effect in 恢复伤害数据
    SourceOut out 修改后的恢复发起者属性
    TargetOut out 修改后的恢复接受者属性
    '''

    script: str

    @clean()
    def serialize(self, where: str = '?') -> dict[str, Any]:
        return {
            **super().serialize(),
            'script': ser_str(self.script, where)
        }


@dataclass(kw_only=True)
class TickScript(Script):
    '''
    Env 环境信息等杂项（等级等）
    SelfIn in 原始的角色数据
    SelfOut out 修改后的角色数据
    '''

    script: str

    delay: int = 0

    interval: int = 1

    times: int = 1

    @clean()
    def serialize(self, where: str = '?') -> dict[str, Any]:
        return {
            **super().serialize(),
            'script': ser_str(self.script, where),
            'delay': ser_int(self.delay, min=0, where=where),
            'interval': ser_int(self.interval, min=0, where=where),
            'times': ser_int(self.times, min=0, where=where),
        }
