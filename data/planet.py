import random
import logging

from .setting import Tags

logger = logging.getLogger("game." + __name__)
logger.setLevel(logging.DEBUG)


class Planet:
    def __init__(self) -> None:
        from .player import Player

        self.number = 0
        self.owner: Player | None = None
        self.broadcasts = []
        self.attacks = []
        self.defense_level = 0
        self.tags = []

    def refresh(self):
        if self.owner is None:
            self.defense_level = 0
            return
        level = 0
        reply = True
        for building in self.owner.buildings:
            level = max(level, building.defense_level)
            if Tags.NO_REPLY in building.tags:
                reply = False
        self.defense_level = level
        if not reply and Tags.NO_REPLY not in self.tags:
            self.tags.append(Tags.NO_REPLY)
        if reply and Tags.NO_REPLY in self.tags:
            self.tags.remove(Tags.NO_REPLY)

    def clear_sun(self):
        self.tags.append(Tags.NO_SUN)
        if self.owner is not None:
            ret = self.owner.destroy_buildings(tags=[Tags.NEED_SUN])
        return ret

    def clear_buildings(self):
        self.tags.append(Tags.NO_BUILDING)
        if self.owner is not None:
            ret = self.owner.destroy_buildings(tags=[Tags.ALL])
        return ret

    def clear_existing(self):
        self.tags.append(Tags.NO_EXISTING)
        if self.owner is not None:
            ret = self.owner.destroy_buildings(tags=[Tags.ALL])
            self.owner.live = False
        return ret


class PlanetMap:
    def __init__(self) -> None:
        self.planets = [Planet() for _ in range(random.randint(7, 11))]
        self.count = len(self.planets)
        for i, planet in enumerate(self.planets):
            planet.number = i + 1
        self.map = {}
        for i in range(1, self.count + 1):
            for j in range(1, self.count + 1):
                if i == j:
                    self.map[(i, j)] = 0
                    continue
                if (i, j) not in self.map:
                    dis = random.randint(1, 3)
                    self.map[(i, j)] = dis
                    self.map[(j, i)] = dis
        logger.info(f"add {self.count} planets,map:{self.map}")


if __name__ == "__main__":
    a = PlanetMap()
