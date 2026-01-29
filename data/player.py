import logging
from typing import Callable, Literal


logger = logging.getLogger("game." + __name__)
logger.setLevel(logging.DEBUG)


function_ID: dict[str, dict[str, Callable]] = {}
"""
start_game: Callable[[Player], None]
start_round: Callable[[Player], None]
apply_attack: Callable[Attack], bool]
other_operation: Callable[[Operation], None]
"""
id_player: dict[str, "Player"] = {}


class Player:
    def __init__(self):
        global Message, Planet, Game, Card, Building, Message, Attack, Broadcast, BuildingCard, AttackCard, BroadcastCard, OperationCard, Card, ADD_ENERGY_ROUNDS, CARDS_NUMBER, Tags, ATTACK_EXISTENCE_ROUNDS, BROADCAST_EXISTENCE_ROUNDS
        from .planet import Planet
        from .game import Game
        from .card import Card
        from .building import Building
        from .message import Message
        from .attack import Attack
        from .building import Building
        from .broadcast import Broadcast
        from .card import (
            BuildingCard,
            AttackCard,
            BroadcastCard,
            OperationCard,
            Card,
        )
        from .setting import (
            ADD_ENERGY_ROUNDS,
            CARDS_NUMBER,
            Tags,
            ATTACK_EXISTENCE_ROUNDS,
            BROADCAST_EXISTENCE_ROUNDS,
        )

        self.planet: Planet | None = None
        self.number: int = 0
        self.game: Game | None = None
        self.live = True
        self.energy = 3
        self.cards: list[Card] = []
        self.buildings: list[Building] = []
        self.attacks: list[Attack] = []
        self.broadcasts: list[Broadcast] = []
        self.connect_ID: str = ""
        self.memories: list[int] = []

    def start_game(self) -> None:
        if not (self.game is not None and self.planet is not None and self.number != 0):
            logger.error(
                f"player属性未初始化{self, self.game, self.planet, self.number}"
            )
            assert False, "player属性未初始化"
        self.cards = []
        while len(self.cards) < CARDS_NUMBER:
            self.cards.append(self.game.get_free_card())
        for id in function_ID:
            if id_player.get(id, None) is None and self.connect_ID == "":
                self.connect_ID = id
                id_player[id] = self
                break
        if self.connect_ID in function_ID:
            functions = function_ID[self.connect_ID]
        else:
            functions = {}
        if (
            functions.get("start_game", None) is not None
            and functions["start_game"] is not None
        ):
            functions["start_game"](self)
        else:
            logger.warning("玩家无start_game函数")

    def build_building(self, cards_ID: int) -> tuple[bool, str]:
        if self.planet is None:
            return False, "玩家属性未初始化"
        if not self.live:
            return False, "玩家已出局"
        if not (0 <= cards_ID < len(self.cards)):
            return False, "卡牌不存在"
        card = self.cards[cards_ID]
        if not isinstance(card, BuildingCard):
            return False, "该卡牌不是建筑卡"
        if Tags.ONLY_ONE in card.tags:
            for building in self.buildings:
                if isinstance(building, type(card)):
                    return False, "该建筑只能建造一次"
        if self.energy < card.cost:
            return False, "能量不足"
        new_building_type: type[Building] | None = card.building
        if new_building_type is None:
            return False, "建筑未知"
        if Tags.NO_BUILDING in self.planet.tags:
            return False, "该星系禁止建造建筑"
        if Tags.NEED_SUN in card.tags and Tags.NO_SUN in self.planet.tags:
            return False, "该星系无太阳能，无法建造该建筑"
        new_building = new_building_type()
        new_building.player = self
        self.buildings.append(new_building)
        self.energy -= card.cost
        self.cards.remove(card)
        if self.game is not None:
            self.game.add_operation(Message(Tags.BUILD, self, (new_building,)))
        else:
            logger.warning("玩家无game属性")
        return True, "建造成功"

    def destroy_buildings(
        self,
        tags: list["Tags"] | None = None,
        building_id: int | None = None,
        is_self=True,
    ):
        if building_id is not None:
            if 0 <= building_id < len(self.buildings):
                destroyed: list[Building] = [self.buildings.pop(building_id)]
                if is_self:
                    self.energy += sum(building.cost // 2 for building in destroyed)
            return destroyed
        destroyed: list[Building] = []
        if tags is not None:
            remaining: list[Building] = []
            for building in self.buildings:
                if any(tag in building.tags for tag in tags) or Tags.ALL in tags:
                    destroyed.append(building)
                else:
                    remaining.append(building)
            self.buildings = remaining
        if is_self:
            self.energy += sum(building.cost // 2 for building in destroyed)
        if self.game is not None:
            self.game.add_operation(Message(Tags.DESTROY, self, (destroyed,)))
        else:
            logger.warning("玩家无game属性")
        return destroyed

    def attack(self, card_number, planet_number: int) -> tuple[bool, str]:
        if self.game is None or self.planet is None or self.number == 0:
            return False, "玩家属性未初始化"
        if all(
            planet_number != planet.number for planet in self.game.planet_map.planets
        ):
            return False, "星球不存在"
        if not (0 <= card_number < len(self.cards)):
            return False, "卡牌不存在"
        card: Card = self.cards[card_number]
        planet = [
            planet
            for planet in self.game.planet_map.planets
            if planet.number == planet_number
        ][0]
        if not isinstance(card, AttackCard):
            return False, "该卡牌不是攻击卡"
        if self.energy < card.cost:
            return False, "能量不足"
        attack_type: type[Attack] | None = card.attack
        if attack_type is None:
            return False, "攻击未知"
        attack = attack_type()
        attack.player = self
        attack.planet = planet
        attack.round = self.game.round
        self.attacks.append(attack)
        planet.attacks.append(attack)
        self.energy -= card.cost
        self.cards.remove(card)
        self.game.add_operation(Message(Tags.ATTACK, self, (attack,)))
        return True, "攻击成功"

    def broadcast(self, card_number: int, planet_number: int) -> tuple[bool, str]:
        if self.game is None or self.planet is None or self.number == 0:
            return False, "玩家属性未初始化"
        if all(
            planet_number != planet.number for planet in self.game.planet_map.planets
        ):
            return False, "星球不存在"
        if not (0 <= card_number < len(self.cards)):
            return False, "卡牌不存在"
        card: Card = self.cards[card_number]
        planet = [
            planet
            for planet in self.game.planet_map.planets
            if planet.number == planet_number
        ][0]
        if not isinstance(card, BroadcastCard):
            return False, "该卡牌不是广播卡"
        if self.energy < card.cost:
            return False, "能量不足"
        broadcast_type: type[Broadcast] | None = card.broadcast
        if broadcast_type is None:
            return False, "广播未知"
        if (
            self.game.planet_map.map.get((self.planet.number, planet.number), None)
            is None
        ):
            return False, "星球不可达"
        if (
            self.game.planet_map.map.get((self.planet.number, planet.number), -1)
            > card.broadcast_range
            and card.broadcast_range != -1
        ):
            return False, "广播距离超出范围"
        broadcast = broadcast_type()

        broadcast.player = self
        broadcast.planet = planet
        self.broadcasts.append(broadcast)
        planet.broadcasts.append(broadcast)
        broadcast.round = self.game.round
        self.energy -= card.cost
        self.cards.remove(card)
        self.game.add_operation(Message(Tags.BROADCAST, self, (broadcast,)))
        return True, "广播成功"

    def respond_broadcast(
        self, card_number: int, planet_number: int
    ) -> tuple[bool, str]:
        if self.game is None or self.planet is None or self.number == 0:
            return False, "玩家属性未初始化"
        if all(
            planet_number != planet.number for planet in self.game.planet_map.planets
        ):
            return False, "星球不存在"
        if not (0 <= card_number < len(self.cards)):
            return False, "卡牌不存在"
        card: Card = self.cards[card_number]
        planet = [
            planet
            for planet in self.game.planet_map.planets
            if planet.number == planet_number
        ][0]
        if not isinstance(card, BroadcastCard):
            return False, "该卡牌不是广播卡"
        broadcast_type: type[Broadcast] | None = card.broadcast
        if broadcast_type is None:
            return False, "广播未知"
        if (
            self.game.planet_map.map.get((self.planet.number, planet.number), None)
            is None
        ):
            return False, "星球不可达"
        if (
            self.game.planet_map.map.get((self.planet.number, planet.number), -1)
            > card.broadcast_range
            and card.broadcast_range != -1
        ):
            return False, "广播距离超出范围"

        broadcast = broadcast_type()

        if card.cost > self.energy:
            return False, "能量不足"
        self.energy -= card.cost
        self.cards.remove(card)

        broadcast.player = self
        broadcast.planet = planet
        self.broadcasts.append(broadcast)
        planet.broadcasts.append(broadcast)

        broadcast2: Broadcast | None = (
            self.planet.broadcasts[0] if len(self.planet.broadcasts) > 0 else None
        )
        if broadcast2 is None:
            return False, "没有可响应的广播"

        message = broadcast.respond(broadcast2)
        message2 = broadcast2.respond(broadcast)
        self.game.add_operation(
            Message(
                Tags.RESPOND_BROADCAST, self, (broadcast, broadcast2, message, message2)
            )
        )
        return True, message

    def operate(self, Card_ID: int):
        if self.game is None or self.planet is None or self.number == 0:
            return False, "玩家属性未初始化"
        if not (0 <= Card_ID < len(self.cards)):
            return False, "卡牌不存在"
        card: Card = self.cards[Card_ID]
        if not isinstance(card, OperationCard):
            return False, "该卡牌不是操作卡"
        if self.energy < card.cost:
            return False, "能量不足"
        self.energy -= card.cost
        self.cards.remove(card)
        result = card.operate(self)
        if self.game is not None:
            self.game.add_operation(Message(Tags.OPERATE, self, (card, result)))
        else:
            logger.warning("玩家无game属性")
        return True, "操作成功"

    def discard(
        self, card_number: int
    ) -> (
        tuple[Literal[False], None, Literal["卡牌不存在"]]
        | tuple[Literal[True], "Card", Literal["卡牌已丢弃"]]
    ):
        if not (0 <= card_number < len(self.cards)):
            return False, None, "卡牌不存在"
        card: Card = self.cards.pop(card_number)
        if self.game is not None:
            self.game.add_operation(Message(Tags.DISCARD, self, (card,)))
        else:
            logger.warning("玩家无game属性")
        return True, card, "卡牌已丢弃"

    def start_round(self) -> None:
        if (
            self.game is None
            or self.planet is None
            or self.number == 0
            or not self.live
        ):
            return
        if self.connect_ID in function_ID:
            functions = function_ID[self.connect_ID]
        else:
            functions = {}
        self.energy += ADD_ENERGY_ROUNDS
        for building in self.buildings:
            building.update()
        self.apply_attacks(functions)
        if "start_round" in functions and functions["start_round"] is not None:
            functions["start_round"](self)
        else:
            logger.warning("玩家无start_round函数")

    def apply_attacks(self, functions: dict[str, Callable]) -> None:
        if (
            self.game is None
            or self.planet is None
            or self.number == 0
            or not self.live
        ):
            return
        for attack in self.attacks:
            if self.game.round - attack.round <= ATTACK_EXISTENCE_ROUNDS:
                if (
                    "apply_attack" in functions
                    and functions["apply_attack"] is not None
                ):
                    ret = functions["apply_attack"](attack)
                else:
                    ret = False
                if ret:
                    attack.allow_attack()
                else:
                    if self.game.round - attack.round == ATTACK_EXISTENCE_ROUNDS:
                        attack.refuse_attack()

    def other_operation(self, operation: "Message") -> None:
        if operation.player == self:
            return
        if self.connect_ID in function_ID:
            functions = function_ID[self.connect_ID]
        else:
            functions = {}
        if functions.get("other_operation", None) is not None:
            functions["other_operation"](operation)
        else:
            logger.warning("玩家无other_operation函数")

    def get_basic_info(self) -> dict:
        if self.game is None or self.planet is None or self.number == 0:
            assert False, "玩家属性未初始化"
        return {
            "player_count": self.game.count,
            "player_id": self.number,
            "planet_info": self.game.planet_map.map,
        }
