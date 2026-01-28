from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    from .player import Player
    from .setting import Tags

    Tag: Tags | None = None
    player: Player | None = None
    result: tuple[Any, ...] = ()
