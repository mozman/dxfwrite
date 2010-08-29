#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: setup
# Created: 14.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='dxfwrite',
    version='0.3.4',
    description='A Python library to create DXF R12 drawings.',
    author='mozman',
    url='http://bitbucket.org/mozman/dxfwrite',
    author_email='mozman@gmx.at',
    packages=['dxfwrite', 'dxfwrite/algebra'],
    provides=['dxfwrite'],
    long_description=read('README'),
    platforms="OS Independent",
    license="GPLv3",
    classifiers=[
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]
     )
