#!/usr/bin/env python3
# encoding: utf8
import os
from io import open
from setuptools import find_packages, setup

current_path = os.path.abspath(os.path.dirname(__file__))

version = "0.1.1"

try:
    with open(os.path.join(current_path, "README.org"), "r", encoding="utf-8") as f:
        readme = f.read()
except FileNotFoundError:
    readme = ""

REQUIRES = ["click", "click-log", "pendulum"]

description = (
    """Transform stationXML files to update embargo policy"""
)

kwargs = {
    "name": "eida_embargo_roller",
    "version": version,
    "description": description,
    "long_description": readme,
    "long_description_content_type": "text/plain",
    "author": "Jonathan Schaeffer",
    "author_email": "dc@resif.fr",
    "maintainer": "Résif-DC",
    "maintainer_email": "dc@resif.fr",
    "url": "https://github.com/EIDA/embargo-roller/",
    "license": "GPLv3",
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    "install_requires": REQUIRES,
    "packages": find_packages(exclude=("tests", "tests.*")),
    "include_package_data": True,
    "entry_points": """
        [console_scripts]
        eida_embargo_roller=src.cli:cli
    """,
}

setup(**kwargs)
