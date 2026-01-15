#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三体游戏主程序入口
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """主函数"""
    print("三体游戏启动中...")
    print("当前Python版本:", sys.version)
    
    # TODO: 游戏初始化逻辑
    # TODO: 游戏主循环


if __name__ == "__main__":
    main()