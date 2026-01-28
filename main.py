#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gevent
import gevent.monkey

gevent.monkey.patch_all()

from data import game, player
import logging
import os, time
import threading

log_format = (
    "%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s:%(funcName)s] %(message)s"
)
log_datefmt = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger("game")


class LowerLevelFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = record.levelname.lower()
        return super().format(record)


file_handler = logging.FileHandler("log/game.log", mode="w", encoding="utf-8")
file_handler.setFormatter(LowerLevelFormatter(log_format, log_datefmt))
logger.addHandler(file_handler)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# 在所有 monkey_patch 完成后才导入 ConnectManager
from data.connect_manager import ConnectManager, Handler

connect_manager = ConnectManager()
logger.info(f"子日志{logging.RootLogger.getChildren}")

# 创建 ThreadPool 用于运行 input()
from gevent.threadpool import ThreadPool

input_pool = ThreadPool(1)


def run_game_logic():
    """在主线程的 gevent 事件循环中运行游戏逻辑"""
    logger.info("等待服务器启动...")
    gevent.sleep(1)  # 等待服务器启动

    start = False
    num_players = -1

    # 只在开始时清屏一次
    clear_screen()
    print("欢迎来到黑暗森林!")

    while start == False:
        if num_players == -1:
            print("\n请说一下一共几个人 (2-4):")
            try:
                # 在线程池中运行 input()，避免阻塞 gevent 事件循环
                num_players_str = input_pool.spawn(input, "> ").get()
                if num_players_str is None:
                    raise ValueError("输入为空")
                num_players = int(num_players_str)
                if num_players < 2 or num_players > 4:
                    print("错误数字，请重新输入！")
                    num_players = -1
            except ValueError:
                print("错误数字，请重新输入！")
        else:
            # 使用 \r 回车符覆盖同一行来更新信息，减少闪烁
            import sys

            sys.stdout.write(
                f"\r当前有{connect_manager.preparing_count}/{num_players}人参加游戏！"
            )
            sys.stdout.flush()

            if connect_manager.preparing_count == num_players:
                start = True
                print("\n游戏开始！")
            else:
                time.sleep(0.5)  # 减少 CPU 占用

    players = [player.Player() for i in range(num_players)]
    g = game.Game(players)
    g.start()


# 在主线程中运行服务器
logger.info("启动服务器...")
server_greenlet = gevent.spawn(connect_manager.run)

# 在主线程的 gevent 事件循环中运行游戏逻辑
game_greenlet = gevent.spawn(run_game_logic)

# 等待服务器或游戏逻辑完成
gevent.joinall([server_greenlet, game_greenlet])
