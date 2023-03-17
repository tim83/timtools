"""Manager for the python package"""

from pathlib import Path

import toml
from setuptools import setup

pyproject_path = Path(__file__).parent / "pyproject.toml"
with open(pyproject_path, "r", encoding="utf-8") as fobj:
    toml_str = fobj.read()
    parsed_toml = toml.loads(toml_str)

setup(
    name="timtools",
    version=parsed_toml["tool"]["poetry"]["version"],
    packages=["timtools"],
    url="https://github.com/tim83/timtools",
    license="",
    author="Tim Mees",
    author_email="tim@mees.vip",
    description="",
    install_requires=["validators", "python-telegram-bot"],
    include_package_data=True,
)
