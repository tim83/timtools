#! /usr/bin/python3
"""Manager for the python package"""

from setuptools import setup

setup(
    name="timtools",
    version="1.0.4",
    packages=["timtools"],
    url="https://github.com/tim83/timtools",
    license="",
    author="Tim Mees",
    author_email="tim@mees.vip",
    description="",
    install_requires=["validators", "python-telegram-bot"],
    include_package_data=True,
)
