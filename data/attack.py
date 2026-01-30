from .setting import Tags
from .message import Message
import logging

logger = logging.getLogger("game." + __name__)
logger.setLevel(logging.DEBUG)


class Attack:
    def __init__(self):
        from .planet import Planet
        from .player import Player

        self.name: str = ""
        self.planet: Planet | None = None
        self.player: Player | None = None
        self.round: int = 0
        self.attack_power: int = 0
        self.tags: tuple[Tags, ...] = ()

    def allow_attack(self) -> tuple[bool, list, str]:
        if self.planet is None or self.player is None:
            return False, [], "攻击属性未初始化"
        if self in self.planet.attacks:
            self.planet.attacks.remove(self)
        else:
            logger.warning("攻击不在星球攻击列表中")
        if self in self.player.attacks:
            self.player.attacks.remove(self)
        else:
            logger.warning("攻击不在玩家攻击列表中")
        if self.player.game is None:
            return False, [], "游戏未初始化"
        else:
            self.player.game.add_operation(
                Message(Tags.ALLOW_ATTACK, self.player, (self,))
            )
        
        ret = []

        if Tags.NO_SUN in self.tags:
            ret = self.planet.clear_sun()
        if Tags.NO_BUILDING in self.tags:
            ret = self.planet.clear_buildings()
        if Tags.NO_EXISTING in self.tags:
            ret = self.planet.clear_existing()
        if Tags.NO_CARD in self.tags:
            if self.planet.owner is not None:
                ret = self.planet.owner.cards
                self.planet.owner.cards.clear()
        if Tags.STILL_LIVE in self.tags:
            return True, ret, "目标玩家仍然存活"

        if self.attack_power > self.planet.defense_level or self.attack_power == -1:
            if self.planet.owner is not None:
                self.planet.owner.live = False
                if (
                    self.player.game is not None
                    and self.planet.owner in self.player.game.live_players
                ):
                    self.player.game.live_players.remove(self.planet.owner)
                    self.player.energy += 3 * len(self.player.game.live_players)
                    for a in self.planet.owner.attacks:
                        a.refuse_attack()

                    if len(self.player.game.live_players) == 1:
                        self.player.game.add_message(
                            Message(Tags.WIN, self.player.game.live_players[0], ())
                        )
                        self.player.game.status = "end"
                return True, ret, "目标玩家被击败"
        else:
            return False, ret, "防御成功"
        return False, ret, "攻击未生效"

    def refuse_attack(self) -> bool:
        if self.planet is None or self.player is None:
            logger.error("攻击属性未初始化")
            assert False, "攻击属性未初始化"
        if self in self.planet.attacks:
            self.planet.attacks.remove(self)
        else:
            logger.warning("攻击不在星球攻击列表中")
        if self in self.player.attacks:
            self.player.attacks.remove(self)
        else:
            logger.warning("攻击不在玩家攻击列表中")
        return True


class ThermonuclearStrike(Attack):
    def __init__(self):
        super().__init__()
        self.name = "热核打击"
        self.attack_power = 1


class PhotonStrike(Attack):
    def __init__(self):
        super().__init__()
        self.name = "光粒打击"
        self.attack_power = 2
        self.tags = (Tags.NO_SUN,)


class AnnihilationStrike(Attack):
    def __init__(self):
        super().__init__()
        self.name = "湮灭打击"
        self.attack_power = 3
        self.tags = (Tags.NO_BUILDING,)


class DimensionalStrike(Attack):
    def __init__(self):
        super().__init__()
        self.name = "降维打击"
        self.attack_power = -1
        self.tags = (Tags.NO_EXISTING,)


class TechnologyLockdown(Attack):
    def __init__(self):
        super().__init__()
        self.name = "科技锁死"
        self.attack_power = -1
        self.tags = (
            Tags.STILL_LIVE,
            Tags.NO_CARD,
        )
