import random
import logging
from typing import Literal
from .planet import PlanetMap
from .player import Player
from .card import create_card_deck
from .message import Message
from .setting import Tags

logger = logging.getLogger("game." + __name__)
logger.setLevel(logging.DEBUG)


class Game:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.live_players = players.copy()
        self.now_player = 1
        self.planet_map = PlanetMap()
        self.free_planets = self.planet_map.planets.copy()
        self.count = len(players)
        self.round = 1
        self.cards = create_card_deck()
        self.operations: list[Message] = []
        self.status: Literal["preparation", "start", "middle", "end"] = "preparation"
        self.messages: list[Message] = []

    def start(self):
        numbers = [i for i in range(1, self.count + 1)]
        random.shuffle(numbers)
        random.shuffle(self.free_planets)
        self.status = "start"
        for player in self.players:
            player.number = numbers.pop()
            player.planet = self.free_planets.pop()
            player.game = self
            player.planet.owner = player

        self.players.sort(key=lambda x: x.number)

        for player in self.players:
            player.start_game()

        self.continue_round()

    def continue_round(self):
        self.status = "middle"
        while self.status == "middle":
            self.start_round()
            self.round += 1
        if self.status == "end":
            self.end_game()
        else:
            assert False, "异常结束"

    def end_game(self):
        for message in self.messages:
            if message.Tag == Tags.WIN:
                win_message = message
                break
        for player in self.players:
            player.other_operation(Message(Tags.WIN, None, (win_message.player,)))

    def start_round(self):
        self.now_player = 1
        while self.status == "middle" and self.now_player <= self.count:
            player = self.players[self.now_player - 1]
            player.start_round()
            self.now_player += 1

    def get_free_card(self):
        if len(self.cards) == 0:
            self.cards = create_card_deck()
            self.add_operation(Message(Tags.ADD_CARD, None, ()))
        r = random.choice(self.cards)
        self.cards.remove(r)
        logger.debug(f"get_free_card: {r}")
        return r

    def add_operation(self, operation: Message):
        self.operations.append(operation)
        for player in self.players:
            player.other_operation(operation)

    def add_message(self, message: Message):
        self.messages.append(message)
