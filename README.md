# 三体游戏 - 代号：黑暗森林

基于《三体》小说改编的桌游《代号：黑暗森林》的Python实现项目。

## 项目简介

这是一个基于刘慈欣科幻小说《三体》改编的策略桌游模拟项目。游戏灵感来源于三体中的黑暗森林理论：宇宙就像是一片黑暗的森林，其中的每个文明都是一个带枪的猎人，为了生存，猎人们都必须时刻"隐藏自己，做好清理"。

## 游戏特色

- **策略性玩法**: 3-5名玩家对战，每局游戏约30分钟
- **卡牌系统**: 包含广播牌、打击牌、建设牌、操作牌等多种卡牌类型
- **建筑系统**: 建造太阳能阵列、聚变反应堆、戴森球等建筑提升文明实力
- **黑暗森林机制**: 广播坐标、打击文明、隐藏自己等核心玩法
- **回合制战斗**: 每回合摸牌、出牌、攻击、建设等完整游戏流程

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

```bash
python main.py
```

## 游戏配置

- **玩家数量**: 标准星图支持 3-5 名玩家对战
- **游戏时长**: 视人数不同，每局游戏时长约 30 分钟
- **每回合摸牌**: 4 张
- **初始能量**: 3 能量

## 项目结构

```
DarkForestProtocol/
├── main.py                   # 主程序入口
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
│   ├── 黑暗森林_游戏规则.md # 游戏规则文档
│   └── __pycache__/         # Python缓存
├── image/                   # 游戏图片资源
├── log/                     # 日志文件目录
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
项目使用Python标准logging模块，日志文件位于 `log/game.log`。

日志格式：
```
%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s:%(funcName)s] %(message)s
```

## 游戏规则

详细游戏规则请参考 `data/黑暗森林_游戏规则.md` 文件。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请通过GitHub Issues联系。