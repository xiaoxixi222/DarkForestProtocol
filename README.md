# 三体游戏 (Three Body Game)

基于《三体》小说的Python游戏项目。

## 项目简介

这是一个基于刘慈欣科幻小说《三体》改编的Python游戏项目。游戏将模拟三体世界的混沌运动和文明演化。

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

## 项目结构

```
three_body_game/
├── main.py              # 主程序入口
├── requirements.txt     # 项目依赖
├── setup.py            # 安装配置
├── .gitignore          # Git忽略文件
└── README.md           # 项目说明
```

## 开发计划

- [ ] 实现三体运动模拟
- [ ] 设计游戏界面
- [ ] 添加文明演化机制
- [ ] 实现游戏控制逻辑
- [ ] 添加音效和音乐

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！