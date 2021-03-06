#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Isomer - The distributed application framework
# ==============================================
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

"""
Schema: Session
===============

Contains
--------

Session: Generic object to store data about lectures, lightning talks etc. 


"""

from isomer.schemata.defaultform import editbuttons, section, lookup_field
from isomer.schemata.base import base_object, uuid_object

SessionSchema = base_object('session',
                            roles_create='crew',
                            roles_list=['admin', 'chair'],
                            roles_read=['admin', 'chair'],
                            roles_write=['admin', 'chair'])

SessionSchema['properties'].update({
    'sessiontype': uuid_object('Session Type', 'Select a session type'),
    'name': {
        'type': 'string', 'title': 'Title',
        'description': 'Title of session'
    },
    'abstract': {
        'type': 'string', 'title': 'Abstract',
        'format': 'html',
        'description': 'Abstract description'
    },
    'keywords': {
        'type': 'string', 'title': 'Keywords',
        'description': 'Space or comma separated descriptive keywords'
    },
    'topics': {
        'type': 'string', 'title': 'Topics',
        'description': 'Space or comma separated list of session Topics'
    },
    'speakers': {
        'type': 'array',
        'title': 'Speakers',
        'description': 'Speakers holding the session (leave empty if it is only you)',
        'default': [],
        'startEmpty': True,
        'items': {
            'type': 'string'
        }
    },
    'files': {
        'type': 'array', 'title': 'Attachments',
        'description': 'Attached files',
        'default': [],
        'items': {
            'type': 'object',
            'properties': {
                'filename': {'type': 'string'},
                'uuid': uuid_object(display=False)
            }

        }
    },
    # 'calendar_reference': uuid_object(title='Calendar')
})

SessionForm = [
    'name',
    section(1, 2, [[
        {'key': 'speakers', 'add': 'Add Speaker', 'startEmpty': True},
        'topics'
    ]]),
    'abstract',
    section(1, 2, [[lookup_field('sessiontype', 'sessiontype'), 'keywords']]),
    {
        'key': 'files',
        'add': None,
        'remove': None,
        'startEmpty': True
    },
]

Session = {'schema': SessionSchema, 'form': SessionForm}
