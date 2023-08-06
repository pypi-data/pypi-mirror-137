#!/usr/bin/env python
from setuptools import setup

setup(
    name="target-streamduo",
    version="0.1.0",
    description="Singer.io target sending data to StreamDuo platform",
    author="StreamDuo",
    url="https://streamduo.com",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["target_streamduo"],
    install_requires=[
        "singer-python==5.0.12",
        "streamduo==0.0.22"
    ],
    entry_points="""
    [console_scripts]
    target-streamduo=target_streamduo:main
    """,
    packages=["target_streamduo"],
    package_data = {},
    include_package_data=True,
)
