#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = "0.1.{}".format(os.getenv('BUILD_VER'))

setup(
    name="circle-ci-icq8680-test",
    version=__version__,
    scripts=['test.py'],
    license="none",
    description="testing python build",
    long_description="I really have nothing to share with you, sorry",
    author="Ramazan Ibragimov",
    author_email="icq8680@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "requests",
        "pyyaml",
    ],
    zip_safe=False,
    package_data={"": ["README.md"]},
)
