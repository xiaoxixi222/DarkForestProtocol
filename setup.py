from setuptools import setup, find_packages

setup(
    name="three-body-game",
    version="0.1.0",
    description="基于《三体》小说的Python游戏",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.13",
    install_requires=[
        "pygame>=2.5.0",
        "numpy>=1.24.0",
        "pyyaml>=6.0",
        "loguru>=0.7.0",
        "typing-extensions>=4.8.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.13",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)