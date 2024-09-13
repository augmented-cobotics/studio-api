#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import re
import sys

requirements = [
    'requests>=2.20.0,<3.0',
    'python-dateutil'
]


setup(
    name='acobotics',
    version='1.0.0',
    description='Augmented Cobotics Studio Python API',
    long_description="""
Augmented Cobotics Studio Python API

This library is used for developing plugins in the Studio app
    """,
    author='Augmented Cobotics',
    author_email='dev@augmentedcobotics.com',
    url='https://github.com/augmented-cobotics/studio-api',
    packages=[
        'acobotics', 'acobotics.api', 'acobotics.plugin'
    ],
    keywords='contentful delivery cda cms content',
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=[
        "pydantic>=1.7.4,!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0",
    ]
)