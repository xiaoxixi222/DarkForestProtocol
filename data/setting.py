from enum import Enum, auto
from pathlib import Path


class Tags(Enum):
    NEED_SUN = auto()
    ONLY_ONE = auto()
    ALL = auto()

    NO_SUN = auto()
    NO_BUILDING = auto()
    NO_EXISTING = auto()
    NO_REPLY = auto()
    STILL_LIVE = auto()
    NO_CARD = auto()

    ATTACK = auto()
    ALLOW_ATTACK = auto()
    REFUSE_ATTACK = auto()
    BUILD = auto()
    DESTROY = auto()
    BROADCAST = auto()
    RESPOND_BROADCAST = auto()
    END_BROADCAST = auto()
    OPERATE = auto()
    DISCARD = auto()
    WIN = auto()
    ADD_CARD = auto()


CARDS_NUMBER = 4

ATTACK_EXISTENCE_ROUNDS = 1
BROADCAST_EXISTENCE_ROUNDS = 3
ADD_ENERGY_ROUNDS = 1

RULE_PATH = Path("data/黑暗森林_游戏规则.md")
COMMANDS = Path("data/command.txt")
