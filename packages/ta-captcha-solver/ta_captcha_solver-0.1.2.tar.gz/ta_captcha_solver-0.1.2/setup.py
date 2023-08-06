#!/usr/bin/env python

"""The setup script."""
import sys

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = []

test_requirements = [
    "pytest>=3",
]

setup(
    author="Bohdan Sukhov",
    author_email="bohdan.sukhov@thoughtfulautomation.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Thoughtful Automation BitWarden CLI installation package",
    entry_points={
        "console_scripts": [
            "ta_captcha_solver=ta_captcha_solver.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="ta_captcha_solver",
    name="ta_captcha_solver",
    packages=find_packages(include=["ta_captcha_solver", "ta_captcha_solver.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://www.thoughtfulautomation.com/",
    version="0.1.2",
    zip_safe=False,
)
