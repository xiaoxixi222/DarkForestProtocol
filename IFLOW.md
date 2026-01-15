# 项目概述

这是一个基于《三体》小说的Python游戏项目，目前处于初始化阶段。

## 项目信息

- **项目名称**: 三体游戏 (Three Body Game)
- **项目类型**: Python游戏项目
- **Python版本**: 3.13.0
- **虚拟环境**: `.venv`

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

## 项目结构

```
三体桌游/
├── .git/              # Git仓库目录
├── .venv/             # Python虚拟环境
└── IFLOW.md           # 项目说明文档
```

## 开发指南

### 安装依赖

当项目有`requirements.txt`文件时，使用以下命令安装依赖：

```powershell
pip install -r requirements.txt
```

### 运行项目

项目目前处于初始化阶段，具体的运行命令待项目开发完成后确定。

## 注意事项

- 始终在激活虚拟环境的情况下进行开发
- 使用Python 3.13.0进行开发
- 定期提交代码到Git仓库
- 项目目录建议重命名为英文名`three-body-game`以避免编码问题