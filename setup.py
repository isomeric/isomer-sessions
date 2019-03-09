#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Isomer Application Framework
# ============================
# Copyright (C) 2011-2019 Heiko 'riot' Weinen <riot@c-base.org> and others.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Heiko 'riot' Weinen"
__license__ = "AGPLv3"

from setuptools import setup, find_packages

setup(
    name="isomer-sessions",
    version="0.0.2",
    description="isomer-sessions",
    author="Isomer Community",
    author_email="riot@c-base.org",
    url="https://github.com/isomeric/isomer-sessions",
    license="GNU Affero General Public License v3",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Isomer :: 1',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',

    ],
    packages=find_packages(),
    include_package_data=True,
    long_description="""Isomer - Sessions
=================

Session objects and management for lectures, lightning talks etc

This software package is a plugin module for Isomer.
""",
    dependency_links=[],
    install_requires=['isomer>=1.0.0'],
    entry_points="""[isomer.components]
      sessionmanager=isomer.sessions.sessionmanager:SessionManager
      [isomer.schemata]
    session=isomer.sessions.session:Session
    sessiontype=isomer.sessions.sessiontype:SessionType
    review=isomer.sessions.review:Review
      [isomer.provisions]
    sessions=isomer.sessions.provisions.sessions_volume:provision
    """,
    test_suite="tests.main.main",
)
