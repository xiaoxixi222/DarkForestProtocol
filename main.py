#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from data import game,player
import logging
import pdb
import sys

log_format = (
    "%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s:%(funcName)s] %(message)s"
)
log_datefmt = "%Y-%m-%d %H:%M:%S"
"""
try:
    import coloredlogs

    coloredlogs.install(
        level="DEBUG",
        fmt=log_format,
        datefmt=log_datefmt,
        level_styles={
            "debug": {"color": "cyan"},
            "info": {"color": "green"},
            "warning": {"color": "yellow"},
            "error": {"color": "red"},
            "critical": {"color": "red", "bold": True},
        },
    )
except ImportError:
    # 如果没有coloredlogs，使用基本格式
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=log_datefmt,
        stream=sys.stdout,
    )"""
logger = logging.getLogger("game")
class LowerLevelFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = record.levelname.lower()
        return super().format(record)
file_handler = logging.FileHandler("log/game.log", mode="w", encoding="utf-8")
file_handler.setFormatter(LowerLevelFormatter(log_format, log_datefmt))
logger.addHandler(file_handler)

g = game.Game([player.Player() for _ in range(4)])
g.start()
