"""
测试示例文件
"""
import pytest


def test_example():
    """示例测试函数"""
    assert 1 + 1 == 2


@pytest.mark.skip(reason="测试框架已设置，等待实际测试用例")
def test_placeholder():
    """占位测试，等待实际测试用例"""
    pass