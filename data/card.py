from typing import Any
from .setting import Tags
from .building import Building
from . import building
from .attack import Attack
from . import attack
from .broadcast import Broadcast
from . import broadcast


class Card:
    count = 0

    def __init__(self):
        self.name: str = ""
        self.english_name: str = ""
        self.description: str = ""
        self.categories: str = ""
        self.effect: str = ""
        self.cost: int = 0
        self.tags: tuple[Tags, ...] = ()


class BuildingCard(Card):
    def __init__(self):
        super().__init__()
        self.defense_level = 0
        self.building: type[Building] | None = None


class AttackCard(Card):
    def __init__(self):

        super().__init__()
        self.attack_power = 0
        self.attack: type[Attack] | None = None


class BroadcastCard(Card):
    def __init__(self):
        super().__init__()
        self.broadcast_range = 0
        self.broadcast: type[Broadcast] | None = None


class OperationCard(Card):
    def __init__(self):
        super().__init__()

    def operate(self, player) -> tuple[Any, ...]:
        return ()


# 广播牌
class StellarBroadcastCooperate(BroadcastCard):
    count = 8

    def __init__(self):
        super().__init__()
        self.name = "恒星广播（合作）"
        self.english_name = "Stellar Broadcast (Cooperate)"
        self.description = "以恒星为超级天线，向宇宙发布恒星及功率的电磁波"
        self.categories = "广播牌"
        self.effect = "合作"
        self.cost = 0
        self.broadcast_range = 1
        self.tags = ()
        self.broadcast: type[broadcast.StellarBroadcastCooperate] = (
            broadcast.StellarBroadcastCooperate
        )


class StellarBroadcastDeceive(BroadcastCard):
    count = 5

    def __init__(self):
        super().__init__()
        self.name = "恒星广播（伪装）"
        self.english_name = "Stellar Broadcast (Deceive)"
        self.description = "以恒星为超级天线，向宇宙发布恒星及功率的电磁波"
        self.categories = "广播牌"
        self.effect = "伪装"
        self.cost = 0
        self.broadcast_range = 1
        self.tags = ()
        self.broadcast: type[broadcast.StellarBroadcastDisguise] = (
            broadcast.StellarBroadcastDisguise
        )


class CosmicBroadcastCooperate(BroadcastCard):
    count = 6

    def __init__(self):
        super().__init__()
        self.name = "宇宙广播（合作）"
        self.english_name = "Cosmic Broadcast (Cooperate)"
        self.description = "以简并态物质作为引力波振动弦，向宇宙发射引力波"
        self.categories = "广播牌"
        self.effect = "合作"
        self.cost = 1
        self.broadcast_range = 2
        self.tags = ()
        self.broadcast: type[broadcast.CosmicBroadcastCooperate] = (
            broadcast.CosmicBroadcastCooperate
        )


class CosmicBroadcastDeceive(BroadcastCard):
    count = 4

    def __init__(self):
        super().__init__()
        self.name = "宇宙广播（伪装）"
        self.english_name = "Cosmic Broadcast (Deceive)"
        self.description = "以简并态物质作为引力波振动弦，向宇宙发射引力波"
        self.categories = "广播牌"
        self.effect = "伪装"
        self.cost = 1
        self.broadcast_range = 2
        self.tags = ()
        self.broadcast: type[broadcast.CosmicBroadcastDisguise] = (
            broadcast.CosmicBroadcastDisguise
        )


class HyperDistanceBroadcastCooperate(BroadcastCard):
    count = 2

    def __init__(self):
        super().__init__()
        self.name = "超距广播（合作）"
        self.english_name = "Hyper-Distance Broadcast (Cooperate)"
        self.description = "利用宇宙的膜结构，在高位空间的投影产生信号的超距通讯"
        self.categories = "广播牌"
        self.effect = "合作"
        self.cost = 2
        self.broadcast_range = -1
        self.tags = ()
        self.broadcast: type[broadcast.HyperDistanceBroadcastCooperate] = (
            broadcast.HyperDistanceBroadcastCooperate
        )


class HyperDistanceBroadcastDeceive(BroadcastCard):
    count = 2

    def __init__(self):
        super().__init__()
        self.name = "超距广播（伪装）"
        self.english_name = "Hyper-Distance Broadcast (Deceive)"
        self.description = "利用宇宙的膜结构，在高位空间的投影产生信号的超距通讯"
        self.categories = "广播牌"
        self.effect = "伪装"
        self.cost = 2
        self.broadcast_range = -1
        self.tags = ()
        self.broadcast: type[broadcast.HyperDistanceBroadcastDisguise] = (
            broadcast.HyperDistanceBroadcastDisguise
        )


# 打击牌
class ThermonuclearStrike(AttackCard):
    count = 4

    def __init__(self):
        super().__init__()
        self.name = "热核打击"
        self.english_name = "Thermonuclear Strike"
        self.description = "向目标行星发射恒星级核弹，造成毁灭性打击"
        self.categories = "打击牌"
        self.effect = "打击不毁灭恒星；可被掩体星环防御"
        self.cost = 4
        self.attack_power = 1
        self.tags = ()
        self.attack: type[attack.ThermonuclearStrike] = attack.ThermonuclearStrike


class PhotonStrike(AttackCard):
    count = 4

    def __init__(self):
        super().__init__()
        self.name = "光粒打击"
        self.english_name = "Photon Strike"
        self.description = "将一个质量点加速至接近光速，使被其撞击的恒星爆发"
        self.categories = "打击牌"
        self.effect = "毁灭目标恒星；可被掩体星环防御"
        self.cost = 6
        self.attack_power = 2
        self.tags = ()
        self.attack: type[attack.PhotonStrike] = attack.PhotonStrike


class AnnihilationStrike(AttackCard):
    count = 3

    def __init__(self):
        super().__init__()
        self.name = "湮灭打击"
        self.english_name = "Annihilation Strike"
        self.description = (
            "反物质导弹到达目标星系时，会发生完全的质能转换，湮灭一切物质"
        )
        self.categories = "打击牌"
        self.effect = "无论是否被防御，均毁灭目标恒星及所有建造牌"
        self.cost = 8
        self.attack_power = 3
        self.tags = (Tags.NO_BUILDING,)
        self.attack: type[attack.AnnihilationStrike] = attack.AnnihilationStrike


class DimensionalStrike(AttackCard):
    count = 3

    def __init__(self):
        super().__init__()
        self.name = "降维打击"
        self.english_name = "Dimensional Strike"
        self.description = '发射二向箔将目标星系空间维度降低，进行彻底"清理"'
        self.categories = "打击牌"
        self.effect = "彻底清除目标星系"
        self.cost = 10
        self.attack_power = -1
        self.tags = (Tags.NO_EXISTING,)
        self.attack: type[attack.DimensionalStrike] = attack.DimensionalStrike


class TechnologyLockdown(AttackCard):
    count = 1

    def __init__(self):
        super().__init__()
        self.name = "科技锁死"
        self.english_name = "Technology Lockdown"
        self.description = "将微观粒子雕刻成超级计算机，干扰目标星系的基础物理研究"
        self.categories = "打击牌"
        self.effect = "打击生效时，目标星系玩家需弃掉手中所有建造牌，不影响其生存"
        self.cost = 4
        self.attack_power = -1
        self.tags = (
            Tags.STILL_LIVE,
            Tags.NO_CARD,
        )
        self.attack: type[attack.TechnologyLockdown] = attack.TechnologyLockdown


# 建设牌
class SolarArray(BuildingCard):
    count = 7

    def __init__(self):
        super().__init__()
        self.name = "太阳能阵列"
        self.english_name = "Solar Array"
        self.description = "建设太阳能风帆阵列以吸收恒星辐射的能量"
        self.categories = "建设牌"
        self.effect = "每回合开始时，能量 +1；依赖恒星"
        self.cost = 2
        self.defense_level = 0
        self.tags = (Tags.NEED_SUN,)
        self.building: type[Building] = building.SolarArray


class FusionReactor(BuildingCard):
    count = 3

    def __init__(self):
        super().__init__()
        self.name = "聚变反应堆"
        self.english_name = "Fusion Reactor"
        self.description = "利用可控核聚变产生能量"
        self.categories = "建设牌"
        self.effect = "每回合开始时，能量 +1；不依赖恒星"
        self.cost = 3
        self.defense_level = 0
        self.tags = ()
        self.building: type[Building] = building.FusionReactor


class AntimatterEngine(BuildingCard):
    count = 3

    def __init__(self):
        super().__init__()
        self.name = "反物质引擎"
        self.english_name = "Antimatter Engine"
        self.description = "利用反物质湮灭产生能量"
        self.categories = "建设牌"
        self.effect = "每回合开始时，能量 +2；不依赖恒星"
        self.cost = 6
        self.defense_level = 0
        self.tags = ()
        self.building: type[Building] = building.AntimatterEngine


class DysonSphere(BuildingCard):
    count = 3

    def __init__(self):
        super().__init__()
        self.name = "戴森球"
        self.english_name = "Dyson Sphere"
        self.description = "完全包围恒星并获得其绝大部分能量输出的巨型结构"
        self.categories = "建设牌"
        self.effect = "每回合开始时，能量 +3；依赖恒星，每个星系只能建造 1 个"
        self.cost = 6
        self.defense_level = 0
        self.tags = (Tags.ONLY_ONE, Tags.NEED_SUN)
        self.building: type[Building] = building.DysonSphere


class ShelterRing(BuildingCard):
    count = 6

    def __init__(self):
        super().__init__()
        self.name = "掩体星环"
        self.english_name = "Shelter Ring"
        self.description = "在巨行星背阳面建设的太空城，可躲避光粒打击引发的恒星爆发"
        self.categories = "建设牌"
        self.effect = "可在等级 2 及以下的打击中幸存"
        self.cost = 6
        self.defense_level = 2
        self.tags = ()
        self.building: type[Building] = building.ShelterRing


class QuantumGhost(BuildingCard):
    count = 3

    def __init__(self):
        super().__init__()
        self.name = "量子幽灵"
        self.english_name = "Quantum Ghost"
        self.description = (
            "文明个体全部被量子化后进入量子态，以概率云米散开，不再需要以实体形式存在"
        )
        self.categories = "建设牌"
        self.effect = "可在等级 3 及以下的打击中幸存"
        self.cost = 8
        self.defense_level = 3
        self.tags = ()
        self.building: type[Building] = building.QuantumGhost


class ListeningBase(BuildingCard):
    count = 2

    def __init__(self):
        super().__init__()
        self.name = "监听基地"
        self.english_name = "Listening Base"
        self.description = '"不要回答、不要回答、不要回答"'
        self.categories = "建设牌"
        self.effect = "所在星系接收广播后可不做回应"
        self.cost = 2
        self.defense_level = 0
        self.tags = (Tags.NO_REPLY,)
        self.building: type[Building] = building.ListeningBase


class LightSpeedShip(OperationCard):
    count = 2

    def __init__(self):
        super().__init__()
        self.name = "光速飞船"
        self.english_name = "Light Speed Ship"
        self.description = "操纵时空曲率从而可以达到光速的飞船，可逃离任意打击"
        self.categories = "建设牌"
        self.effect = "可跃迁至随机其他星系，不能携带能量和建造牌，且只能使用 1 次"
        self.cost = 10
        self.defense_level = 0
        self.tags = (Tags.ONLY_ONE,)


def get_all_card_classes():
    """获取所有卡牌类"""
    return [
        StellarBroadcastCooperate,
        StellarBroadcastDeceive,
        CosmicBroadcastCooperate,
        CosmicBroadcastDeceive,
        HyperDistanceBroadcastCooperate,
        HyperDistanceBroadcastDeceive,
        ThermonuclearStrike,
        PhotonStrike,
        AnnihilationStrike,
        DimensionalStrike,
        TechnologyLockdown,
        SolarArray,
        FusionReactor,
        AntimatterEngine,
        DysonSphere,
        ShelterRing,
        QuantumGhost,
        LightSpeedShip,
        ListeningBase,
    ]


def create_card_deck():
    """创建完整的卡牌堆"""
    deck = []
    for card_class in get_all_card_classes():
        for _ in range(card_class.count):
            deck.append(card_class())
    return deck
