# gevent.monkey.patch_all() 已在 main.py 中调用
from typing import Any, Literal
from flask import Flask
import socketio as socketio_lib
import logging
from gevent.event import Event

from data.building import Building
from data.card import Card

logger = logging.getLogger("game." + __name__)
logger.setLevel(logging.DEBUG)

from .message import Message
from .player import Player
from .attack import Attack
from .setting import RULE_PATH, COMMANDS


class ConnectManager:

    def __init__(self, host="localhost", port=9000):

        # 配置 Flask 日志 - 关闭控制台输出，只输出到文件
        werkzeug_logger = logging.getLogger("werkzeug")
        werkzeug_logger.setLevel(logging.DEBUG)  # 只记录错误级别

        # 将 Flask 日志输出到文件
        file_handler = logging.FileHandler("log/flask.log")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        werkzeug_logger.addHandler(file_handler)
        logger.info(
            f'Flask 日志输出到文件: "log/flask.log" handlers:{werkzeug_logger.handlers}'
        )
        logger.debug(
            f"Flask 日志级别: {werkzeug_logger.level}handlers级别:{','.join(str(h.level) for h in werkzeug_logger.handlers)}"
        )

        # 创建 Flask 应用
        self.app = Flask(__name__)
        # 创建 Socket.IO 服务器，禁用 WebSocket，只使用 HTTP polling
        self.sio = socketio_lib.Server(
            cors_allowed_origins="*",
            async_mode="gevent",
            websocket=False,  # 禁用 WebSocket
        )
        # 将 Socket.IO 附加到 Flask 应用
        self.app.wsgi_app = socketio_lib.WSGIApp(self.sio, self.app.wsgi_app)

        self.host: str = host
        self.port: int = port  # 转换为整数

        # 在创建 WSGIApp 之前注册所有事件处理器
        self._register_handlers()

        self.sid_ID_map: dict[int, str | None] = {}  # 记录 sid 和 ID 的映射关系
        self.ID_handler_map: dict[str, Handler] = {}  # 记录 ID 和 handler 的映射关系
        self.connect_count = 0  # 记录当前连接数
        self.preparing_count = 0  # 记录当前准备连接数

        from .player import function_ID

        self.function_map = function_ID

    def _register_handlers(self):
        """注册所有 Socket.IO 事件处理器"""

        # 注册 connect 事件
        def connect(sid, environ):
            logger.info(f"✓ 客户端连接: {sid}   {environ}")
            self.connect_count += 1

        self.sio.on("connect", connect)

        # 注册 disconnect 事件
        def disconnect(sid):
            logger.info(f"✗ 客户端断开: {sid}")
            id = self.sid_ID_map.get(sid, None)
            if id is not None:
                self.preparing_count -= 1
            self.sid_ID_map[sid] = None
            self.connect_count -= 1

        self.sio.on("disconnect", disconnect)

        # 注册 prepare_connect 事件
        def prepare_connect(sid, data):
            logger.info(f"收到 prepare_connect: {sid}, 数据: {data}")
            id = data["ID"]
            # 检查客户端ID是否已经存在
            if id in self.sid_ID_map.values():
                logger.info(f"客户端ID已存在: {id}")
                self.sio.emit("output", "该客户端已经启动", to=sid)
                self.sio.emit("disconnect", to=sid)
                return
            self.sid_ID_map[sid] = id
            self.preparing_count += 1
            if self.ID_handler_map.get(id, None) is not None:
                logger.info(f"handler 已存在: {id}")
                handler = self.ID_handler_map[id]
                handler.sid = sid
                self.refresh_function_map()
                if not handler.receive_event.is_set():
                    handler.send_event("input", None)
                return
            if data["type"] == "people":
                handler = Handler(id, self.sio, sid, self)
            else:
                logger.error(f"未知的连接类型: {data['type']}")
                assert False, "未知的连接类型"
            self.ID_handler_map[id] = handler
            self.refresh_function_map()

        self.sio.on("prepare_connect", prepare_connect)

        # 注册 send_input 事件
        def send_input(sid, data):
            logger.info(f"收到 send_input: {sid}, 数据: {data}")
            id: str | None = self.sid_ID_map.get(sid, None)
            if id is None:
                logger.error(f"未知的 sid: {sid}")
                return
            handler: Handler | None = self.ID_handler_map.get(id, None)
            if handler is None:
                logger.error(f"未知的 handler: {id}")
                return
            handler.receive = data
            handler.receive_event.set()

        self.sio.on("send_input", send_input)

    def run(self):
        """在主线程中运行服务器"""
        self.init()

    def init(self):
        # 使用 gevent.pywsgi 启动服务器
        from gevent.pywsgi import WSGIServer

        logger.info(f"准备启动 Socket.IO 服务器...")
        logger.info(f"  Host: {self.host}")
        logger.info(f"  Port: {self.port}")
        logger.info(f"  Async Mode: gevent")
        logger.info(f"  App: {self.app}")
        logger.info(f"  SIO: {self.sio}")
        logger.info(f"  WSGI App: {self.app.wsgi_app}")
        logger.info(
            f"  已注册的事件处理器: {list(self.sio.handlers.keys()) if hasattr(self.sio, 'handlers') else '未知'}"
        )

        logger.info(f"✓ Socket.IO 服务器启动在 {self.host}:{self.port}")
        logger.info(f"✓ 等待客户端连接...")

        try:
            from geventwebsocket.handler import WebSocketHandler

            WSGIServer(
                (self.host, self.port), self.app, handler_class=WebSocketHandler
            ).serve_forever()
        except Exception as e:
            logger.error(f"服务器启动失败: {e}")
            import traceback

            traceback.print_exc()
            raise

    def refresh_function_map(self):
        for id, handler in self.ID_handler_map.items():
            self.function_map[id] = {
                "start_game": handler.start_game,
                "start_round": handler.start_round,
                "apply_attack": handler.apply_attack,
                "other_operation": handler.other_operation,
            }


class Handler:
    def __init__(
        self,
        ID: str,
        sio: socketio_lib.Server,
        sid: int,
        connection_manager: ConnectManager,
    ):
        self.ID = ID
        self.sio = sio
        self.sid = sid
        self.connection_manager = connection_manager
        self.receive = ""
        # 使用 gevent.event.Event，因为游戏逻辑在主线程的 gevent 事件循环中运行
        self.receive_event = Event()
        self.receive_event.set()

    def start_game(self, player: Player):
        self.output("开始游戏")
        rule: str = RULE_PATH.read_text(encoding="utf-8")
        basic_info: dict = player.get_basic_info()
        basic_info["player_count"] = str(basic_info["player_count"])
        basic_info["player_id"] = str(basic_info["player_id"])
        s: str = ""
        for k, v in basic_info["planet_info"].items():
            s += f"{k[0]}到{k[1]}的距离为{v}\n"
        basic_info["planet_info"] = s
        rule = rule.format(**basic_info)
        self.output(rule)
        commands: str = COMMANDS.read_text(encoding="utf-8")
        self.output(commands)

    def start_round(self, player: Player):
        self.output("开始回合\n请选择行动")
        while True:
            output = f"当前能源：{player.energy}, {("星系"+str(player.planet.number) if player.planet is not None else '无星系')}, 卡牌："
            for i, card in enumerate(player.cards):
                output += f"{card.name}({card.cost}, {i}号) "
            self.output(output)
            ret = self.input().split(" ")
            long = len(ret)
            if long == 0:
                self.output("输入错误，请重新输入")
            elif ret[0] == "exit" and long == 1:
                self.output("退出游戏")
                self.send_event("ask_disconnect", None)
            elif ret[0] == "clear" and long == 1:
                self.output("清除屏幕")
                self.send_event("clear", None)
            elif ret[0] == "build" and long == 2:
                build_ret: tuple[bool, str] = player.build_building(int(ret[1]))
                if build_ret[0]:
                    output = f"建造成功, {build_ret[1]}"
                else:
                    output = f"建造失败: {build_ret[1]}"
                self.output(output)
            elif ret[0] == "destroy" and long == 2:
                destroy_ret: list[Building] = player.destroy_buildings(
                    building_id=int(ret[1])
                )
                output = f"摧毁建筑:{",".join(b.name for b in destroy_ret)}"
                self.output(output)
            elif ret[0] == "attack" and long == 3:
                attack_ret: tuple[bool, str] = player.attack(int(ret[1]), int(ret[2]))
                if attack_ret[0]:
                    output = f"攻击成功, {attack_ret[1]}"
                else:
                    output = f"攻击失败: {attack_ret[1]}"
                self.output(output)
            elif ret[0] == "broadcast" and long == 3:
                broadcast_ret: tuple[bool, str] = player.broadcast(
                    int(ret[1]), int(ret[2])
                )
                if broadcast_ret[0]:
                    output = f"广播成功, {broadcast_ret[1]}"
                else:
                    output = f"广播失败: {broadcast_ret[1]}"
                self.output(output)
            elif ret[0] == "respond_broadcast" and long == 3:
                respond_broadcast_ret: tuple[bool, str] = player.respond_broadcast(
                    int(ret[1]), int(ret[2])
                )
                if respond_broadcast_ret[0]:
                    output = f"回应广播成功, {respond_broadcast_ret[1]}"
                else:
                    output = f"回应广播失败: {respond_broadcast_ret[1]}"
                self.output(output)
            elif ret[0] == "operate" and long == 2:
                operation_ret: tuple[bool, str] = player.operate(int(ret[1]))
                if operation_ret[0]:
                    output = f"操作成功, {operation_ret[1]}"
                else:
                    output = f"操作失败: {operation_ret[1]}"
                self.output(output)
            elif ret[0] == "discard" and long == 2:
                discard_ret: tuple[bool, Card | None, str] = player.discard(int(ret[1]))
                if discard_ret[0]:
                    if discard_ret[1] is None:
                        output = f"丢弃卡牌成功, {discard_ret[2]}"
                    else:
                        output = (
                            f"丢弃卡牌成功, {discard_ret[1].name}, {discard_ret[2]}"
                        )
                else:
                    output = f"丢弃卡牌失败: {discard_ret[2]}"
                self.output(output)
            elif ret[0] == "end_turn" and long == 1:
                self.output("结束回合")
                break
            else:
                self.output("输入错误，请重新输入")

    def apply_attack(self, attack: Attack):
        self.output(f"攻击: {attack.name}是否允许?(y/n)")
        ret = self.input()
        if ret == "y":
            return True
        elif ret == "n":
            return False
        else:
            return False

    def other_operation(self, operation: Message):
        self.output(f"收到其他操作: {message_to_str(operation)}")

    def output(self, message: str):
        logger.info(f"发送消息: {message}")
        self.sio.emit("output", message, to=self.sid)

    def input(self):
        self.receive_event.clear()
        self.sio.emit("input", to=self.sid)
        self.receive_event.wait()
        logger.info(f"收到消息: {self.receive}")
        return self.receive

    def send_event(self, event: str, data: Any = None):
        self.sio.emit(event, data, to=self.sid)


def message_to_str(message: Message) -> str:
    """将 Message 对象转换为友好的中文描述

    Args:
        message: Message 对象

    Returns:
        中文描述字符串
    """
    from .setting import Tags

    if message.Tag is None:
        return "未知操作"

    # 获取玩家信息
    player_info = ""
    if message.player is not None:
        player_info = f"玩家{message.player.number}"

    # 根据 Tag 生成不同的描述
    tag_descriptions = {
        Tags.ATTACK: "攻击",
        Tags.ALLOW_ATTACK: "同意攻击",
        Tags.REFUSE_ATTACK: "拒绝攻击",
        Tags.BUILD: "建造",
        Tags.DESTROY: "摧毁",
        Tags.BROADCAST: "广播",
        Tags.RESPOND_BROADCAST: "回应广播",
        Tags.OPERATE: "操作",
        Tags.DISCARD: "弃牌",
        Tags.WIN: "胜利",
        Tags.ADD_CARD: "获得卡牌",
    }

    tag_desc = tag_descriptions.get(message.Tag, str(message.Tag))

    # 根据结果生成详细描述
    if not message.result:
        if player_info:
            return f"{player_info}进行了{tag_desc}"
        return tag_desc

    # 解析 result 生成详细描述
    result_desc = ""
    if message.Tag == Tags.ATTACK and len(message.result) > 0:
        attack = message.result[0]
        planet_info = f"在{attack.planet.number}号星球上" if attack.planet else ""
        result_desc = f"释放了{attack.name}{planet_info}"
    elif message.Tag == Tags.ALLOW_ATTACK and len(message.result) > 0:
        attack = message.result[0]
        planet_info = f"在{attack.planet.number}号星球上" if attack.planet else ""
        # 计算距离
        distance_info = ""
        if (
            attack.player
            and attack.player.planet
            and attack.planet
            and attack.player.game
        ):
            distance = attack.player.game.planet_map.map.get(
                (attack.player.planet.number, attack.planet.number), 0
            )
            distance_info = f"（距离{distance}）"
        result_desc = f"确认{attack.name}{planet_info}{distance_info}"
    elif message.Tag == Tags.BUILD and len(message.result) > 0:
        building = message.result[0]
        result_desc = f"建造了{building.name}"
    elif message.Tag == Tags.BROADCAST and len(message.result) > 0:
        broadcast = message.result[0]
        planet_info = f"在{broadcast.planet.number}号星球上" if broadcast.planet else ""
        result_desc = f"发出了{broadcast.name}{planet_info}"
    elif message.Tag == Tags.DESTROY and len(message.result) > 0:
        target = message.result[0]
        result_desc = f"摧毁了{target.name}"
    elif message.Tag == Tags.RESPOND_BROADCAST and len(message.result) >= 4:
        broadcast1 = message.result[0]
        broadcast2 = message.result[1]
        message1 = message.result[2]
        message2 = message.result[3]
        planet_info = f"在{broadcast2.planet.number}号星球" if broadcast2.planet else ""
        result_desc = f"使用{broadcast1.name}{planet_info}回应{broadcast2.name}: {message1}, 对方回应: {message2}"
    elif message.Tag == Tags.OPERATE and len(message.result) >= 2:
        card = message.result[0]
        result_str = message.result[1]
        result_desc = f"使用了{card.name}: {result_str}"
    elif message.Tag == Tags.DISCARD and len(message.result) > 0:
        card = message.result[0]
        result_desc = f"弃掉了{card.name}"
    else:
        # 默认处理：将 result 转换为字符串
        result_desc = str(message.result)

    if player_info and result_desc:
        return f"{player_info}{result_desc}"
    elif player_info:
        return f"{player_info}进行了{tag_desc}"
    elif result_desc:
        return result_desc
    return tag_desc


if __name__ == "__main__":
    cm = ConnectManager()
