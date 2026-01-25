import logging

from .setting import Tags

logger = logging.getLogger("game." + __name__)


class Building:
    def __init__(self):
        from .player import Player

        self.name = ""
        self.player: Player | None = None
        self.defense_level = 0
        self.cost = 0
        self.tags: tuple[Tags, ...] = ()

    def update(self):
        if self.player is None:
            logger.error("building属性未初始化")
            assert False, "building属性未初始化"


class SolarArray(Building):
    def __init__(self):
        super().__init__()
        self.name = "太阳能阵列"
        self.defense_level = 0
        self.cost = 2
        self.tags = (Tags.NEED_SUN,)

    def update(self):
        if self.player is None:
            logger.error("building属性未初始化")
            assert False, "building属性未初始化"
        self.player.energy += 1


class FusionReactor(Building):
    def __init__(self):
        super().__init__()
        self.name = "聚变反应堆"
        self.defense_level = 0
        self.cost = 3
        self.tags = ()

    def update(self):
        if self.player is None:
            logger.error("building属性未初始化")
            assert False, "building属性未初始化"
        self.player.energy += 1


class AntimatterEngine(Building):
    def __init__(self):
        super().__init__()
        self.name = "反物质引擎"
        self.cost = 6
        self.defense_level = 0
        self.tags = ()

    def update(self):
        if self.player is None:
            logger.error("building属性未初始化")
            assert False, "building属性未初始化"
        self.player.energy += 2


class DysonSphere(Building):
    def __init__(self):
        super().__init__()
        self.name = "戴森球"
        self.cost = 6
        self.defense_level = 0
        self.tags = (Tags.ONLY_ONE, Tags.NEED_SUN)

    def update(self):
        if self.player is None:
            logger.error("building属性未初始化")
            assert False, "building属性未初始化"
        self.player.energy += 3


class ShelterRing(Building):
    def __init__(self):
        super().__init__()
        self.name = "掩体星环"
        self.cost = 6
        self.defense_level = 2
        self.tags = ()


class QuantumGhost(Building):
    def __init__(self):
        super().__init__()
        self.name = "量子幽灵"
        self.cost = 8
        self.defense_level = 3
        self.tags = ()


class ListeningBase(Building):
    def __init__(self):
        super().__init__()
        self.name = "监听基地"
        self.cost = 2
        self.defense_level = 0
        self.tags = (Tags.NO_REPLY,)
