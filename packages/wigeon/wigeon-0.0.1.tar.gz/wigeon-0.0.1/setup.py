#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    path = os.path.join(package, "__init__.py")
    init_py = open(path, "r", encoding="utf8").read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_long_description():
    """
    Return the README.
    """
    return open("README.md", "r", encoding="utf8").read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]

env_marker_below_38 = "python_version < '3.8'"

minimal_requirements = [
    "click>=8.0.3",
    "typer>=0.4.0",
    "pyodbc>=4.0.32"
]


setup(
    name="wigeon",
    version=get_version("wigeon"),
    url="https://github.com/JLRitch/wigeon",
    license="BSD",
    description="DB Migrations for the continuous developer.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Jere Ritchie",
    author_email="jereritchie@gmail.com",
    packages=get_packages("wigeon"),
    python_requires=">=3.7",
    install_requires=minimal_requirements,
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
    entry_points="""
    [console_scripts]
    wigeon=wigeon.main:app
    """,
    project_urls={
        "Source": "https://github.com/"
    },
)