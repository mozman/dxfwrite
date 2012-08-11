#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: setup
# Created: 14.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

import os
from distutils.core import setup

from dxfwrite import VERSION, AUTHOR_NAME, AUTHOR_EMAIL

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '%s' not found.\n" % fname

setup(name='dxfwrite',
    version=VERSION,
    description='A Python library to create DXF R12 drawings.',
    author=AUTHOR_NAME,
    url='http://bitbucket.org/mozman/dxfwrite',
    download_url='http://bitbucket.org/mozman/dxfwrite/downloads',
    author_email=AUTHOR_EMAIL,
    packages=['dxfwrite', 'dxfwrite/algebra'],
    provides=['dxfwrite'],
    long_description=read('README.txt')+read('NEWS.txt'),
    keywords=['DXF', 'CAD'],
    platforms="OS Independent",
    license="MIT License",
    classifiers=[
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]
     )
