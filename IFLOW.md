# 项目概述

这是一个基于《三体》小说改编的桌游《代号：黑暗森林》的Python实现项目，支持单机和网络多人对战模式。

## 项目信息

- **项目名称**: 三体游戏 - 代号：黑暗森林 (Three Body Game - Dark Forest Protocol)
- **项目类型**: Python桌游模拟项目
- **Python版本**: 3.13.0
- **虚拟环境**: `.venv`
- **许可证**: MIT License
- **Git仓库**: https://github.com/xiaoxixi222/DarkForestProtocol.git

## 游戏背景

游戏灵感来源于三体中的黑暗森林理论：宇宙就像是一片黑暗的森林，其中的每个文明都是一个带枪的猎人，为了生存，猎人们都必须时刻"隐藏自己，做好清理"。

## 环境配置

### 虚拟环境

项目使用Python 3.13.0创建的虚拟环境，位于项目根目录的`.venv`文件夹中。

**激活虚拟环境:**

Windows:
```powershell
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

**退出虚拟环境:**
```powershell
deactivate
```

### Python版本管理

系统同时安装了Python 3.14.0和Python 3.13.0。本项目使用Python 3.13.0。

**检查Python版本:**
```powershell
py -3.13 --version
```

**使用Python 3.13运行脚本:**
```powershell
py -3.13 script.py
```

## 项目依赖

### 核心依赖

- `pygame>=2.5.0` - 游戏开发框架
- `numpy>=1.24.0` - 数据处理
- `pyyaml>=6.0` - 配置文件处理
- `loguru>=0.7.0` - 日志处理
- `typing-extensions>=4.8.0` - 类型检查扩展
- `flask>=3.0.0` - Web框架（网络模式）
- `flask-socketio>=5.3.0` - WebSocket支持（网络模式）
- `python-socketio>=5.10.0` - Socket.IO客户端（网络模式）
- `eventlet>=0.33.0` - 异步网络库（网络模式）

### 安装依赖

```powershell
pip install -r requirements.txt
```

## 项目结构

```
DarkForestProtocol/
├── .git/                  # Git仓库目录
├── .venv/                 # Python虚拟环境
├── .vscode/               # VSCode配置
├── data/                  # 游戏数据模块
│   ├── attack.py          # 攻击类定义
│   ├── broadcast.py       # 广播类定义
│   ├── building.py        # 建筑类定义
│   ├── card.py            # 卡牌类定义
│   ├── client.py          # Socket.IO客户端（网络模式）
│   ├── connect_manager.py # 连接管理器（网络模式）
│   ├── game.py            # 游戏核心逻辑
│   ├── message.py         # 消息系统
│   ├── planet.py          # 星球类定义
│   ├── player.py          # 玩家类定义
│   ├── setting.py         # 游戏设置和常量
│   ├── command.txt        # 命令配置
│   ├── 黑暗森林_游戏规则.md # 游戏规则文档
│   ├── 黑暗森林_游戏规则完整版.md # 完整游戏规则
│   └── __pycache__/       # Python缓存
├── image/                 # 游戏图片资源
├── log/                   # 日志文件目录
├── client1/               # 客户端1目录
│   ├── log/               # 客户端1日志
│   └── setting/           # 客户端1配置
│       └── setting.json   # 客户端ID配置
├── client2/               # 客户端2目录
│   ├── log/               # 客户端2日志
│   └── setting/           # 客户端2配置
│       └── setting.json   # 客户端ID配置
├── setting/               # 配置文件目录
│   └── setting.json       # 默认客户端配置文件
├── tmp/                   # 临时文件目录
├── IFLOW.md               # 项目开发文档
├── LICENSE                # 许可证文件
├── main.py                # 主程序入口
├── README.md              # 项目说明
├── requirements.txt       # 项目依赖
└── setup.py              # 安装配置
```

## 开发指南

### 运行项目

#### 方式一：使用 main.py 启动（推荐）

运行主程序会同时启动服务器和游戏逻辑：

```powershell
python main.py
```

程序会提示输入玩家数量（2-4人），等待所有玩家连接后自动开始游戏。

#### 方式二：分别启动服务器和客户端

**启动服务器:**
```powershell
python -m data.connect_manager
```

**启动客户端:**
```powershell
python -m data.client
```

可以启动多个客户端实例进行测试，每个客户端会自动生成唯一的客户端ID。

### 游戏配置

- **玩家数量**: 标准星图支持 3-5 名玩家对战
- **游戏时长**: 视人数不同，每局游戏时长约 30 分钟
- **每回合摸牌**: 4 张
- **初始能量**: 3 能量

### 卡牌类型

游戏包含以下卡牌类型：

1. **广播牌** (BroadcastCard)
   - 恒星广播（合作/伪装）
   - 宇宙广播（合作/伪装）
   - 超距广播（合作/伪装）

2. **打击牌** (AttackCard)
   - 热核打击
   - 光粒打击
   - 湮灭打击
   - 降维打击
   - 科技锁死

3. **建设牌** (BuildingCard)
   - 太阳能阵列
   - 聚变反应堆
   - 反物质引擎
   - 戴森球
   - 掩体星环
   - 量子幽灵
   - 监听基地

4. **操作牌** (OperationCard)
   - 光速飞船

### 代码架构

#### 核心模块

- **Card**: 卡牌基类，定义卡牌基本属性
- **BuildingCard**: 建筑卡类，绑定对应的Building实例
- **AttackCard**: 攻击卡类，定义攻击力
- **BroadcastCard**: 广播卡类，定义广播范围
- **OperationCard**: 操作卡类，定义操作逻辑

#### 游戏逻辑

- **Game**: 游戏主控制器，管理游戏流程
  - 管理玩家列表和存活玩家
  - 控制游戏状态（preparation, start, middle, end）
  - 管理回合制流程
  - 处理卡牌抽取和分发
  - 管理操作队列和消息系统

- **Player**: 玩家类，管理玩家状态和手牌
  - 管理玩家生命状态（live）
  - 管理能量系统
  - 管理手牌、建筑、攻击、广播
  - 处理回合开始和游戏开始逻辑
  - 支持自定义操作函数（通过function_ID）

- **Planet**: 星球类，管理星球信息和建筑
  - 管理星球所有者
  - 计算防御等级
  - 管理星球标签系统
  - 处理恒星清除等特殊事件

- **Building**: 建筑基类，定义建筑属性和效果
  - 定义建筑防御等级
  - 定义建筑标签系统
  - 定义建筑效果和限制

#### 网络通信模块

- **ConnectManager**: 连接管理器（服务器端）
  - 使用 Flask + Socket.IO 实现WebSocket通信
  - 管理客户端连接和断开
  - 处理玩家准备和消息转发
  - 支持自定义玩家操作函数（Handler）

- **Client**: Socket.IO客户端
  - 自动生成和管理客户端ID
  - 处理服务器消息和用户输入
  - 支持连接、断开和错误处理

- **Handler**: 客户端处理器
  - 实现 start_game、start_round、apply_attack、other_operation 等方法
  - 通过 output/input 与客户端交互

#### 消息转换系统

- **message_to_str**: 将 Message 对象转换为友好的中文描述
  - 支持所有消息类型（ATTACK, BUILD, BROADCAST, DESTROY, RESPOND_BROADCAST, OPERATE, DISCARD, WIN, ALLOW_ATTACK）
  - 自动计算并显示攻击距离（仅在 ALLOW_ATTACK 时）
  - 显示星球编号和玩家信息

- **str_to_message**: 将 JSON 字符串转换为 Message 对象

#### 数据结构

- **Tags**: 游戏标签系统
  - 建筑标签：NEED_SUN, ONLY_ONE, NO_SUN, NO_BUILDING, NO_EXISTING, NO_REPLY, STILL_LIVE, NO_CARD
  - 操作标签：ATTACK, ALLOW_ATTACK, REFUSE_ATTACK, BUILD, DESTROY, BROADCAST, RESPOND_BROADCAST, OPERATE, DISCARD, WIN, ADD_CARD
- **Message**: 消息系统，用于玩家间通信和游戏事件通知
  - 包含标签、玩家、结果等字段
  - 用于广播操作和游戏状态变化
  - RESPOND_BROADCAST 格式: (broadcast1, broadcast2, message1, message2)

#### 游戏常量

- **CARDS_NUMBER**: 每回合摸牌数量（4张）
- **ATTACK_EXISTENCE_ROUNDS**: 攻击存在回合数（1回合）
- **BROADCAST_EXISTENCE_ROUNDS**: 广播存在回合数（3回合）
- **ADD_ENERGY_ROUNDS**: 增加能量回合数（1回合）

### 日志系统

项目使用Python标准logging模块，日志文件位于 `log/` 目录：

- `game.log` - 游戏主日志
- `flask.log` - Flask服务器日志
- `client.log` - 客户端日志

日志格式：
```
%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s:%(funcName)s] %(message)s
```

主程序使用自定义的LowerLevelFormatter，将日志级别转换为小写。

### 游戏流程

1. **游戏初始化** (preparation)
   - 创建游戏实例，传入玩家列表
   - 初始化星球地图和卡牌组

2. **游戏开始** (start)
   - 随机分配玩家编号和星球
   - 按编号排序玩家
   - 调用每个玩家的start_game方法

3. **游戏进行** (middle)
   - 按回合进行游戏
   - 每回合按玩家编号顺序执行
   - 每个玩家执行start_round方法
   - 检查游戏结束条件

4. **游戏结束** (end)
   - 检测获胜玩家
   - 通知所有玩家游戏结果

### 网络模式流程

1. **服务器启动**
   - 创建 ConnectManager 实例
   - 启动 Flask + Socket.IO 服务器
   - 等待客户端连接

2. **客户端连接**
   - 生成或读取客户端ID（存储在 setting.json）
   - 连接到服务器
   - 发送 prepare_connect 消息

3. **游戏进行**
   - 服务器通过 Handler 调用玩家方法
   - Handler 通过 output/input 与客户端交互
   - 消息通过 message_to_str 转换为友好格式显示

4. **断开连接**
   - 客户端主动断开或服务器断开
   - 清理连接状态

## Git仓库

项目已初始化Git仓库，远程仓库地址：https://github.com/xiaoxixi222/DarkForestProtocol.git

**查看Git状态:**
```powershell
git status
```

**查看远程仓库:**
```powershell
git remote -v
```

**添加文件到暂存区:**
```powershell
git add .
```

**提交更改:**
```powershell
git commit -m "提交信息"
```

**推送到远程仓库:**
```powershell
git push origin master
```

## Git工作流程规范

### Issue 格式规范

创建Issue时应遵循以下格式，便于追踪和解决问题：

**标题格式**
```
类型: 简短描述
```

类型包括：
- `Bug`: 错误修复
- `Feat`: 新功能
- `Refactor`: 重构
- `Docs`: 文档
- `Test`: 测试
- `Chore`: 构建/工具

**Issue 内容模板**
```markdown
**问题描述**
简要描述问题的现象和影响

**复现步骤**
1. 步骤一
2. 步骤二
3. ...

**预期行为**
描述应该发生的正确行为

**实际行为**
描述实际发生的错误行为

**影响范围**
- 影响的模块/功能
- 影响的用户场景

**建议修复**
提供修复建议或解决方案思路

**环境信息**
- Python版本
- 操作系统
- 相关依赖版本
```

**示例**
```markdown
**问题描述**
在 data/connect_manager.py 中，prepare_connect 事件处理中没有判断 uuid 是否已经加入，导致同一个客户端开两个进程来加入游戏时会被误判成两个玩家。

**复现步骤**
1. 启动服务器
2. 使用同一个客户端ID开两个进程来加入游戏
3. 两个进程都会被记录为独立的玩家
4. 但因为接入时只看ID，实际只有一个玩家参与游戏
5. 导致找不到第二个玩家，报错

**预期行为**
服务器应该检测到重复的客户端ID，拒绝重复连接或提示用户

**实际行为**
相同的客户端ID被多次记录为独立玩家，导致游戏执行时玩家数量不匹配

**影响范围**
- 影响多人游戏的正常进行
- 可能导致游戏无法开始或崩溃

**建议修复**
在 `prepare` 事件处理中添加对uuid的去重检查，确保每个客户端ID只能被加入一次
```

### Commit 格式规范

提交信息应遵循以下格式：

**基本格式**
```
类型(范围): 简短描述

详细描述（可选）

影响范围（可选）

Closes #issue编号
```

**类型（Type）**
- `Fix`: 修复bug
- `Feat`: 新功能
- `Refactor`: 重构（不改变功能）
- `Docs`: 文档更新
- `Test`: 测试相关
- `Chore`: 构建/工具/依赖
- `Style`: 代码风格（不影响功能）
- `Perf`: 性能优化

**范围（Scope）**
- 描述修改的模块或文件
- 例如：`player`, `connect_manager`, `game`

**详细描述**
- 多行时每行不超过72个字符
- 说明"为什么"修改，而不是"做了什么"
- 可以包含多个段落

**影响范围**
- 列出受影响的模块、方法或文件
- 便于追踪和审查

**示例**
```
Fix: 修复广播范围判断错误（and改成or）

问题：
- 广播范围判断逻辑错误，使用or运算符导致所有广播都会被判为范围不足
- 当 broadcast_range 为 -1 时违反第一个条件
- 当 broadcast_range 不为 -1 时违反第二个条件
- 导致无法正常使用广播功能

原因：
- 代码中使用了 or 运算符而非 and 运算符
- 逻辑应该是：当距离超过范围 且 范围不为 -1 时才判定为超范围

修复：
- 将第209行和第254行的 or 改为 and
- 确保只有当距离真正超出范围时才判定为范围不足

影响：
- data/player.py: broadcast() 和 respond_broadcast() 方法

Fixes #6
```

### PR（Pull Request）格式规范

创建PR时应遵循以下格式：

**标题格式**
```
类型: 简短描述
```

**PR 内容模板**
```markdown
**概述**
简要描述本次PR的目的和主要内容

**修复的问题**
1. **Bug #编号**: 问题标题
   - 问题：简要描述
   - 修复：简要说明修复方案

2. **Bug #编号**: 问题标题
   - 问题：简要描述
   - 修复：简要说明修复方案

**影响范围**
- 修改的文件列表
- 影响的模块/功能

**测试建议**
1. 测试场景一
2. 测试场景二
3. ...

**关闭的Issues**
Closes #5, #6, #7, #8, #9
```

**示例**
```markdown
**概述**
本PR修复了游戏中的5个关键bug，包括连接管理、广播范围、回合补牌、攻击显示和能量判断问题。

**修复的问题**

1. **Bug #5**: 防止相同客户端ID重复连接
   - 问题：相同客户端ID开两个进程连接时，会被误判为两个独立玩家
   - 修复：在prepare_connect中添加重复检测，使用.values()检查ID是否已存在

2. **Bug #6**: 修复广播范围判断错误（and改成or）
   - 问题：广播范围判断逻辑错误，使用or运算符导致所有广播都会被判为范围不足
   - 修复：将第209行和第254行的or改为and

3. **Bug #7**: 修复回合开始时没有补牌的问题
   - 问题：补牌逻辑只在游戏开始时执行一次，后续回合不再补牌
   - 修复：在start_round方法中添加补牌逻辑，每个回合开始时补足CARDS_NUMBER张牌

4. **Bug #9**: 修复确认攻击时显示类名而非攻击名称的问题
   - 问题：确认攻击时显示的是对象的内存地址，导致用户无法清楚看到攻击类型
   - 修复：将{attack}改为{attack.name}

5. **Bug #8**: 修复能量判断错误（<=改成<）
   - 问题：能量判断逻辑错误，使用<=运算符导致能量等于消耗时被误判为能量不足
   - 修复：将4处能量判断从<=改为<

**影响范围**
- data/connect_manager.py: prepare_connect和apply_attack方法
- data/player.py: build_building、attack、broadcast、operate、start_round、respond_broadcast方法

**测试建议**
1. 测试相同客户端ID重复连接是否被正确拒绝
2. 测试各种广播卡牌的范围判断是否正确
3. 测试多回合游戏时每回合是否正确补牌
4. 测试攻击确认时是否显示正确的攻击名称
5. 测试能量等于消耗时是否能正常使用卡牌

**关闭的Issues**
Closes #5, #6, #7, #8, #9
```

### 分支管理策略

**主分支**
- `master`: 主分支，始终保持稳定可运行状态
- 所有PR都应该merge到master分支

**功能分支**
- 命名格式：`类型-简短描述`
- 类型前缀：
  - `feature-`: 新功能开发
  - `fix-`: Bug修复
  - `refactor-`: 重构
  - `docs-`: 文档更新
  - `test-`: 测试相关
  - `chore-`: 构建/工具

**示例**
```
feature-logging-enhancement
fix-game-bugs
refactor-card-system
docs-api-guide
```

**分支工作流程**
1. 从master创建新分支
   ```bash
   git checkout master
   git pull origin master
   git checkout -b feature-xxx
   ```

2. 在新分支上进行开发和提交

3. 推送分支到远程
   ```bash
   git push -u origin feature-xxx
   ```

4. 创建PR到master分支

5. Review通过后merge到master

6. 合并后删除功能分支
   ```bash
   git checkout master
   git branch -d feature-xxx
   git push origin --delete feature-xxx
   ```

**注意事项**
- 不要直接在master分支上开发
- 每个功能/修复使用独立分支
- 保持分支粒度适中，避免包含太多改动
- PR描述要清晰，便于Review
- 合并前确保所有测试通过

## 开发规范

### 代码风格

- 使用Python 3.13+类型注解
- 遵循PEP 8代码规范
- 使用类型提示（type hints）提高代码可读性
- 建筑卡通过`building`属性绑定对应的Building类型
- 使用Literal类型定义有限的状态集合

### 模块导入

- 使用相对导入导入同级模块
- 例如：`from .building import Building`
- 例如：`from . import building`
- 避免循环导入，在函数内部导入时使用延迟导入

### 注意事项

- 始终在激活虚拟环境的情况下进行开发
- 使用Python 3.13.0进行开发
- 定期提交代码到Git仓库
- 修改卡牌或建筑类时，确保同步更新对应的绑定关系
- 日志文件位于log目录，注意日志轮转和清理
- Player类支持自定义操作函数，通过function_ID字典注册
- 游戏状态管理使用Literal类型确保类型安全
- 网络模式需要确保服务器和客户端使用相同的端口配置

## 游戏规则详情

详细游戏规则请参考 `data/黑暗森林_游戏规则.md` 文件。

## 扩展开发

### 添加新卡牌

1. 在`card.py`中定义新的卡牌类
2. 在对应的模块（attack.py, building.py, broadcast.py）中实现卡牌效果
3. 在`create_card_deck`函数中添加新卡牌到牌组

### 添加新建筑

1. 在`building.py`中定义新的建筑类
2. 设置建筑的防御等级、标签和效果
3. 创建对应的BuildingCard并绑定建筑实例

### 添加自定义玩家逻辑

1. 创建Player子类或使用function_ID注册自定义函数
2. 重写start_game、start_round等方法
3. 实现apply_attack、other_operation等回调函数

### 扩展网络功能

1. 在 `connect_manager.py` 中添加新的 Socket.IO 事件处理
2. 在 `client.py` 中添加对应的客户端事件监听
3. 在 `Handler` 类中实现新的操作方法
4. 更新 `function_map` 映射关系

## 常见问题

### Q: 如何修改每回合摸牌数量？
A: 修改`setting.py`中的`CARDS_NUMBER`常量。

### Q: 如何修改游戏回合数？
A: 修改`setting.py`中的`ATTACK_EXISTENCE_ROUNDS`、`BROADCAST_EXISTENCE_ROUNDS`等常量。

### Q: 如何添加新玩家？
A: 在`main.py`中修改创建Player实例的数量，传入Game构造函数。

### Q: 如何修改服务器端口？
A: 在启动服务器时修改 `ConnectManager(host="localhost", port=9000)` 中的 port 参数。

### Q: 客户端ID存储在哪里？
A: 客户端ID存储在 `setting/setting.json` 文件中，首次运行时自动生成。

### Q: 如何自定义消息显示格式？
A: 修改 `connect_manager.py` 中的 `message_to_str` 函数。