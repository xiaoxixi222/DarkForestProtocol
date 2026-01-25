# 项目概述

这是一个基于《三体》小说改编的桌游《代号：黑暗森林》的Python实现项目。

## 项目信息

- **项目名称**: 三体游戏 (Three Body Game)
- **项目类型**: Python桌游模拟项目
- **Python版本**: 3.13.0
- **虚拟环境**: `.venv`
- **许可证**: MIT License

## 游戏背景

游戏灵感来源于三体中的黑暗森林理论，宇宙就像是一片黑暗的森林，其中的每个文明都是一个带枪的猎人，为了生存，猎人们都必须时刻"隐藏自己，做好清理"。

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

### 安装依赖

```powershell
pip install -r requirements.txt
```

## 项目结构

```
three_body_game/
├── .git/                  # Git仓库目录
├── .venv/                 # Python虚拟环境
├── .vscode/               # VSCode配置
├── data/                  # 游戏数据模块
│   ├── attack.py          # 攻击类定义
│   ├── broadcast.py       # 广播类定义
│   ├── building.py        # 建筑类定义
│   ├── card.py            # 卡牌类定义
│   ├── game.py            # 游戏核心逻辑
│   ├── planet.py          # 星球类定义
│   ├── player.py          # 玩家类定义
│   ├── setting.py         # 游戏设置和常量
│   ├── 黑暗森林_游戏规则.md # 游戏规则文档
│   └── 卡牌列表.json       # 卡牌数据配置
├── image/                 # 游戏图片资源
├── log/                   # 日志文件目录
├── tmp/                   # 临时文件目录
├── IFLOW.md               # 项目说明文档
├── LICENSE                # 许可证文件
├── main.py                # 主程序入口
├── README.md              # 项目说明
├── requirements.txt       # 项目依赖
└── setup.py              # 安装配置
```

## 开发指南

### 运行项目

```powershell
python main.py
```

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
- **Player**: 玩家类，管理玩家状态和手牌
- **Planet**: 星球类，管理星球信息和建筑
- **Building**: 建筑基类，定义建筑属性和效果

#### 数据结构

- **Tags**: 游戏标签系统（NEED_SUN, ONLY_ONE等）
- **卡牌列表.json**: 卡牌数据配置文件

### 日志系统

项目使用Python标准logging模块，日志文件位于 `log/game.log`。

日志格式：
```
%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s:%(funcName)s] %(message)s
```

## Git仓库

项目已初始化Git仓库。

**查看Git状态:**
```powershell
git status
```

**添加文件到暂存区:**
```powershell
git add .
```

**提交更改:**
```powershell
git commit -m "提交信息"
```

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

### 注意事项

- 始终在激活虚拟环境的情况下进行开发
- 使用Python 3.13.0进行开发
- 定期提交代码到Git仓库
- 修改卡牌或建筑类时，确保同步更新对应的绑定关系
- 日志文件位于log目录，注意日志轮转和清理

## 游戏规则详情

详细游戏规则请参考 `data/黑暗森林_游戏规则.md` 文件。