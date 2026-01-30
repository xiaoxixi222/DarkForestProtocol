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
            ret = self.owner.destroy_buildings(tags=[Tags.NEED_SUN], is_self=False)
            return ret
        return []

    def clear_buildings(self):
        self.tags.append(Tags.NO_BUILDING)
        if self.owner is not None:
            ret = self.owner.destroy_buildings(tags=[Tags.ALL], is_self=False)
            return ret
        return []

    def clear_existing(self):
        self.tags.append(Tags.NO_EXISTING)
        if self.owner is not None:
            ret = self.owner.destroy_buildings(tags=[Tags.ALL], is_self=False)
            self.owner.live = False
            if self.owner.game is not None:
                self.owner.game.free_planets.remove(self)
            return ret
        return []


class PlanetMap:
    def __init__(self) -> None:
        self.count = 9
        self.planets = [Planet() for _ in range(self.count)]
        for i, planet in enumerate(self.planets):
            planet.number = i + 1
        self.map = {  # map[(i,j)]=map[(j,i)]=distance between i and j
            (1, 1): 0,
            (1, 2): 1,
            (1, 3): 1,
            (1, 4): 1,
            (1, 5): 2,
            (1, 6): 2,
            (1, 7): 2,
            (1, 8): 3,
            (1, 9): 3,
            (2, 1): 1,
            (2, 2): 0,
            (2, 3): 2,
            (2, 4): 1,
            (2, 5): 2,
            (2, 6): 1,
            (2, 7): 3,
            (2, 8): 2,
            (2, 9): 3,
            (3, 1): 1,
            (3, 2): 2,
            (3, 3): 0,
            (3, 4): 1,
            (3, 5): 2,
            (3, 6): 3,
            (3, 7): 1,
            (3, 8): 3,
            (3, 9): 2,
            (4, 1): 1,
            (4, 2): 1,
            (4, 3): 1,
            (4, 4): 0,
            (4, 5): 1,
            (4, 6): 2,
            (4, 7): 2,
            (4, 8): 2,
            (4, 9): 3,
            (5, 1): 2,
            (5, 2): 2,
            (5, 3): 2,
            (5, 4): 1,
            (5, 5): 0,
            (5, 6): 1,
            (5, 7): 1,
            (5, 8): 1,
            (5, 9): 1,
            (6, 1): 2,
            (6, 2): 1,
            (6, 3): 3,
            (6, 4): 2,
            (6, 5): 1,
            (6, 6): 0,
            (6, 7): 2,
            (6, 8): 1,
            (6, 9): 2,
            (7, 1): 2,
            (7, 2): 3,
            (7, 3): 1,
            (7, 4): 2,
            (7, 5): 1,
            (7, 6): 2,
            (7, 7): 0,
            (7, 8): 2,
            (7, 9): 1,
            (8, 1): 3,
            (8, 2): 2,
            (8, 3): 3,
            (8, 4): 2,
            (8, 5): 1,
            (8, 6): 1,
            (8, 7): 2,
            (8, 8): 0,
            (8, 9): 1,
            (9, 1): 3,
            (9, 2): 3,
            (9, 3): 2,
            (9, 4): 3,
            (9, 5): 1,
            (9, 6): 2,
            (9, 7): 1,
            (9, 8): 1,
            (9, 9): 0,
        }

        """
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
        """
        logger.info(f"add {self.count} planets,map:{self.map}")


if __name__ == "__main__":
    a = PlanetMap()
