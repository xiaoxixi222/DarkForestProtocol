# 三体游戏 - 代号：黑暗森林

基于《三体》小说改编的桌游《代号：黑暗森林》的Python实现项目，支持单机和网络多人对战模式。

## 项目简介

这是一个基于刘慈欣科幻小说《三体》改编的策略桌游模拟项目。游戏灵感来源于三体中的黑暗森林理论：宇宙就像是一片黑暗的森林，其中的每个文明都是一个带枪的猎人，为了生存，猎人们都必须时刻"隐藏自己，做好清理"。

## 项目信息

- **项目名称**: 三体游戏 - 代号：黑暗森林 (Three Body Game - Dark Forest Protocol)
- **项目类型**: Python桌游模拟项目
- **Python版本**: 3.13.0
- **许可证**: MIT License
- **Git仓库**: https://github.com/xiaoxixi222/DarkForestProtocol.git

## 游戏特色

- **策略性玩法**: 3-5名玩家对战，每局游戏约30分钟
- **卡牌系统**: 包含广播牌、打击牌、建设牌、操作牌等多种卡牌类型
- **建筑系统**: 建造太阳能阵列、聚变反应堆、戴森球等建筑提升文明实力
- **黑暗森林机制**: 广播坐标、打击文明、隐藏自己等核心玩法
- **回合制战斗**: 每回合摸牌、出牌、攻击、建设等完整游戏流程
- **网络对战**: 支持通过 Socket.IO 进行远程多人对战
- **实时通信**: WebSocket 实时消息传递，友好的中文消息显示

## 环境要求

- Python 3.13.0
- pip

## 安装步骤

### 1. 创建虚拟环境

Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux/Mac:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

## 运行游戏

### 单机模式

```bash
python main.py
```

### 网络模式

**启动服务器:**
```bash
python -m data.connect_manager
```

**启动客户端:**
```bash
python -m data.client
```

## 游戏配置

- **玩家数量**: 标准星图支持 3-5 名玩家对战
- **游戏时长**: 视人数不同，每局游戏时长约 30 分钟
- **每回合摸牌**: 4 张
- **初始能量**: 3 能量
- **服务器端口**: 默认 9000（可在 connect_manager.py 中修改）

## 项目结构

```
DarkForestProtocol/
├── main.py                   # 主程序入口（服务器模式）
├── requirements.txt          # 项目依赖
├── setup.py                 # 安装配置
├── LICENSE                  # 许可证文件
├── README.md                # 项目说明
├── IFLOW.md                 # 项目开发文档
├── .gitignore               # Git忽略文件
├── data/                    # 游戏数据模块
│   ├── game.py              # 游戏核心逻辑
│   ├── player.py            # 玩家类定义
│   ├── planet.py            # 星球类定义
│   ├── card.py              # 卡牌基类定义
│   ├── building.py          # 建筑类定义
│   ├── attack.py            # 攻击类定义
│   ├── broadcast.py         # 广播类定义
│   ├── message.py           # 消息系统
│   ├── setting.py           # 游戏设置和常量
│   ├── connect_manager.py   # 连接管理器（网络模式）
│   ├── client.py            # Socket.IO客户端（网络模式）
│   ├── command.txt          # 命令配置
│   ├── 黑暗森林_游戏规则.md # 游戏规则文档
│   ├── 黑暗森林_游戏规则完整版.md # 完整游戏规则
│   └── __pycache__/         # Python缓存
├── client1/                 # 客户端1目录
│   ├── log/                 # 客户端1日志
│   └── setting/             # 客户端1配置
│       └── setting.json     # 客户端ID配置
├── client2/                 # 客户端2目录
│   ├── log/                 # 客户端2日志
│   └── setting/             # 客户端2配置
│       └── setting.json     # 客户端ID配置
├── setting/                 # 配置文件目录
│   └── setting.json         # 默认客户端配置文件
├── image/                   # 游戏图片资源
├── log/                     # 日志文件目录
│   ├── game.log             # 游戏主日志
│   ├── flask.log            # Flask服务器日志
│   └── client.log           # 客户端日志
└── tmp/                     # 临时文件目录
```

## 卡牌系统

### 广播牌 (BroadcastCard)
- 恒星广播（合作/伪装）
- 宇宙广播（合作/伪装）
- 超距广播（合作/伪装）

### 打击牌 (AttackCard)
- 热核打击
- 光粒打击
- 湮灭打击
- 降维打击
- 科技锁死

### 建设牌 (BuildingCard)
- 太阳能阵列
- 聚变反应堆
- 反物质引擎
- 戴森球
- 掩体星环
- 量子幽灵
- 监听基地

### 操作牌 (OperationCard)
- 光速飞船

## 代码架构

### 核心模块
- **Card**: 卡牌基类，定义卡牌基本属性
- **BuildingCard**: 建筑卡类，绑定对应的Building实例
- **AttackCard**: 攻击卡类，定义攻击力
- **BroadcastCard**: 广播卡类，定义广播范围
- **OperationCard**: 操作卡类，定义操作逻辑

### 游戏逻辑
- **Game**: 游戏主控制器，管理游戏流程
- **Player**: 玩家类，管理玩家状态和手牌
- **Planet**: 星球类，管理星球信息和建筑
- **Building**: 建筑基类，定义建筑属性和效果

### 网络通信模块
- **ConnectManager**: 连接管理器（服务器端），使用 Flask + Socket.IO 实现 WebSocket 通信
- **Client**: Socket.IO 客户端，处理服务器消息和用户输入
- **Handler**: 客户端处理器，实现玩家操作方法

### 消息转换系统
- **message_to_str**: 将 Message 对象转换为友好的中文描述
- **str_to_message**: 将 JSON 字符串转换为 Message 对象

### 数据结构
- **Tags**: 游戏标签系统（NEED_SUN, ONLY_ONE等）
- **Message**: 消息系统，用于玩家间通信

## 开发规范

### 代码风格
- 使用Python 3.13+类型注解
- 遵循PEP 8代码规范
- 使用类型提示（type hints）提高代码可读性
- 建筑卡通过`building`属性绑定对应的Building类型

### 模块导入
- 使用相对导入导入同级模块
- 例如：`from .building import Building`
- 例如：`from . import building`

### 日志系统
项目使用Python标准logging模块，日志文件位于 `log/` 目录：

- `game.log` - 游戏主日志
- `flask.log` - Flask服务器日志
- `client.log` - 客户端日志

日志格式：
```
%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s:%(funcName)s] %(message)s
```

## 游戏规则

详细游戏规则请参考 `data/黑暗森林_游戏规则.md` 文件。

## 网络模式说明

网络模式使用 Socket.IO 实现实时通信，支持远程多人对战：

### 启动方式

**方式一：使用 main.py 启动（推荐）**

运行主程序会同时启动服务器和游戏逻辑：
```bash
python main.py
```

**方式二：分别启动服务器和客户端**

1. **启动服务器**: 运行以下命令启动游戏服务器
   ```bash
   python -m data.connect_manager
   ```

2. **启动客户端**: 运行以下命令启动客户端并连接到服务器
   ```bash
   python -m data.client
   ```

### 多客户端支持

项目支持多客户端连接，每个客户端可以独立运行：

- **client1/**: 客户端1的配置和日志目录
- **client2/**: 客户端2的配置和日志目录

每个客户端首次运行时会自动生成唯一ID并保存到对应的 `setting/setting.json` 文件中。

### 实时交互特性

- **WebSocket通信**: 使用 Flask-SocketIO 实现实时双向通信
- **自动重连**: 客户端支持断线重连机制
- **消息同步**: 所有游戏操作和消息通过 WebSocket 实时同步
- **中文显示**: 游戏消息自动转换为友好的中文格式显示

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请通过GitHub Issues联系。