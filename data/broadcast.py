import logging

from .setting import Tags

logger = logging.getLogger("game." + __name__)
logger.setLevel(logging.DEBUG)


class Broadcast:
    def __init__(self):
        from .planet import Planet
        from .player import Player

        self.name: str = ""
        self.planet: Planet | None = None
        self.player: Player | None = None
        self.tags: tuple[Tags, ...] = ()
        self.range: int = 0
        self.cost: int = 0
        self.effect: bool = False  # True:合作 False:伪装
        self.round: int = 0

    def respond(self, broadcast: "Broadcast") -> str:
        if self.planet is None or self.player is None:
            logger.error("广播属性未初始化")
            assert False, "广播属性未初始化"
        if self in self.planet.broadcasts:
            self.planet.broadcasts.remove(self)
        else:
            logger.warning("广播不在星球广播列表中")
        if self in self.player.broadcasts:
            self.player.broadcasts.remove(self)
        else:
            logger.warning("广播不在玩家广播列表中")
        self.player.energy -= self.cost
        if self.effect:
            if broadcast.effect:
                self.player.energy += 3
                return "双方合作，能量+3"
            else:
                return "对方伪装，合作失败"
        else:
            if broadcast.effect:
                self.player.energy += 5
                return "对方合作，能量+5"
            else:
                return "双方伪装，合作失败"


class StellarBroadcastCooperate(Broadcast):
    def __init__(self):
        super().__init__()
        self.tags = ()
        self.name = "恒星广播-合作"
        self.range = 1
        self.cost = 0
        self.effect = True


class StellarBroadcastDisguise(Broadcast):
    def __init__(self):
        super().__init__()
        self.name = "恒星广播-伪装"
        self.tags = ()
        self.range = 1
        self.cost = 0
        self.effect = False


class CosmicBroadcastCooperate(Broadcast):
    def __init__(self):
        super().__init__()
        self.name = "宇宙广播-合作"
        self.tags = ()
        self.range = 2
        self.cost = 1
        self.effect = True


class CosmicBroadcastDisguise(Broadcast):
    def __init__(self):
        super().__init__()
        self.name = "宇宙广播-伪装"
        self.tags = ()
        self.range = 2
        self.cost = 1
        self.effect = False


class HyperDistanceBroadcastCooperate(Broadcast):
    def __init__(self):
        super().__init__()
        self.name = "超距广播-合作"
        self.tags = ()
        self.range = -1
        self.cost = 2
        self.effect = True


class HyperDistanceBroadcastDisguise(Broadcast):
    def __init__(self):
        super().__init__()
        self.name = "超距广播-伪装"
        self.tags = ()
        self.cost = 2
        self.range = -1
        self.effect = False
