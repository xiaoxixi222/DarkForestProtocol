import os
import gevent
import gevent.monkey

gevent.monkey.patch_all()

from pathlib import Path
import socketio
import time
import logging
import uuid
from queue import Queue

log_format = (
    "%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s:%(funcName)s] %(message)s"
)
log_datefmt = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger("client")
logger.setLevel(logging.DEBUG)


class LowerLevelFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = record.levelname.lower()
        return super().format(record)


file_handler = logging.FileHandler("log/client.log", mode="w", encoding="utf-8")
file_handler.setFormatter(LowerLevelFormatter(log_format, log_datefmt))
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
logger.addHandler(console_handler)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class Client:

    def __init__(self, host="localhost", port=9000):
        # 创建客户端，使用 gengine 以与服务器端兼容
        import socketio as sio_lib

        # 使用 gevent 引擎创建客户端
        self.sio = sio_lib.Client(
            reconnection=True,  # 启用自动重连
            reconnection_attempts=5,  # 最大重连次数
            reconnection_delay=3,  # 重连延迟（秒）
        )
        self.host = host
        self.port = port
        logger.info(f"正在初始化客户端: {self.host}:{self.port}")
        self.ID = self.get_ID()

        # 创建队列用于输入请求和响应
        self.input_request_queue = Queue()
        self.input_response_queue = Queue()

        # 创建 ThreadPool 用于运行 input()
        from gevent.threadpool import ThreadPool

        self.input_pool = ThreadPool(1)
        self.init()

    def get_ID(self):
        setting_path = Path("setting") / "setting.json"
        if not setting_path.exists():
            logger.info("正在创建配置文件")
            ID = str(uuid.uuid4())
            if not setting_path.parent.exists():
                setting_path.parent.mkdir()
            with open(setting_path, "x", encoding="utf-8") as f:
                f.write(f'{{"ID": "{ID}"}}')
            return ID
        else:
            logger.info("正在读取配置文件")
            setting = setting_path.read_text()
            setting = eval(setting)
            ID = setting["ID"]
            return ID

    def init(self):
        # 监听连接事件
        @self.sio.event
        def connect():
            logger.info("✓ 已连接到服务器")
            print("连接成功")
            self.sio.emit("prepare_connect", {"type": "people", "ID": self.ID})

        # 监听断开事件
        @self.sio.event
        def disconnect():
            logger.info("✗ 已断开连接")

        # 监听连接错误
        @self.sio.event
        def connect_error(data):
            logger.error(f"✗ 连接错误: {data}")

        @self.sio.event
        def output(data):
            logger.info(f"服务器输出: {data}")
            print(f"{data}")

        @self.sio.event
        def input():
            # 将输入请求放入队列，由主循环处理
            self.input_request_queue.put(True)

        @self.sio.event
        def ask_disconnect():
            logger.info("用户请求断开连接")
            self.sio.disconnect()
            import sys

            sys.exit()

        @self.sio.event
        def clear():
            logger.info("清屏")
            clear_screen()

        # 连接到服务器
        url = f"http://{self.host}:{self.port}"
        logger.info(f"正在连接到: {url}")

        try:
            self.sio.connect(url)
            logger.info(f"✓ 连接成功: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"✗ 连接失败: {e}")
            import traceback

            traceback.print_exc()
            raise  # 抛出异常以触发自动重连机制


if __name__ == "__main__":
    clear_screen()
    client = Client()

    def input_loop():
        """在主循环中处理用户输入"""
        try:
            while True:
                if not client.input_request_queue.empty():
                    # 有输入请求，获取用户输入
                    client.input_request_queue.get()
                    ret = input("> ")
                    logger.info(f"用户输入: {ret}")
                    client.sio.emit("send_input", ret)
                gevent.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("客户端退出")
            client.sio.disconnect()

    # 启动输入循环
    input_greenlet = gevent.spawn(input_loop)

    # 保持客户端运行
    try:
        input_greenlet.join()
    except KeyboardInterrupt:
        logger.info("客户端退出")
        client.sio.disconnect()
