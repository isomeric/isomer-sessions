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
from isomer.misc import std_uuid, std_now

__author__ = "Heiko 'riot' Weinen"
__license__ = "AGPLv3"

"""

Module: Session Manager
=======================

The Session Manager checks and administrates sessions.

"""

import os
from time import time
from dateutil import parser
from datetime import timedelta
from isomer.component import ConfigurableComponent, handler, authorized_event
from isomer.events.client import send
from isomer.database import objectmodels
from isomer.logger import error, warn, hilight, debug, verbose
from circuits import Timer, Event

from isomer.debugger import cli_register_event


# CLI events

class cli_test_Session(Event):
    """Triggers a Session check"""
    pass


class session_attach_file(authorized_event):
    pass


class session_confirm(authorized_event):
    roles = ['chair']


# Components


class SessionManager(ConfigurableComponent):
    """
    Manages Session edits
    """

    configprops = {}
    channel = 'isomer-web'

    def __init__(self, *args):
        super(SessionManager, self).__init__("SESSION", *args)

        self.fireEvent(cli_register_event('test_Session', cli_test_Session))

        self.log("Started")

    @handler("cli_test_Session")
    def cli_test_Session(self, *args):
        """CLI command to ad-hoc test Session"""
        self.log('Checking sessions')

    @handler(session_attach_file)
    def session_attach_file(self, event):
        self.log('Received attachment for session')

        name = event.data['name']
        self.log(name)

        # self.log(event.data['raw'])

        path = os.path.join(self.storagepath, event.user.uuid)
        filename = os.path.join(path, name)
        os.makedirs(path)

        with open(filename, 'wb') as f:
            f.write(event.data['raw'])

        notification = {
            'component': 'isomer.session.manager',
            'action': 'session_attach_file',
            'data': {
                'msg': 'Attachement stored',
                'type': 'success'
            }
        }
        self.fireEvent(send(event.client.uuid, notification))

    @handler(session_confirm)
    def session_confirm(self, event):
        self.log('Confirmation for session received', event.__dict__)

        session_uuid = event.data.get('session', None)
        calendar_uuid = event.data.get('calendar', None)
        # session_time = parser.parse(event.data.get('time', None))

        session = objectmodels['session'].find_one({'uuid': session_uuid})
        calendar = objectmodels['calendar'].find_one({'uuid': calendar_uuid})

        session_type = objectmodels['sessiontype'].find_one({'uuid': session.sessiontype})

        # session_end = (session_time + timedelta(minutes=session_type.length)).isoformat()
        # session_time = session_time.isoformat()

        summary_data = {
            'author': [],
            'event_type': session_type.name,
            'event_id': 'ABC',
            'event_keywords': session.keywords,
            'event_topics': session.topics,
            'abstract': session.abstract,
            'keywords': "",
            'topics': "",
            'speakers': "",
            'size': 3
        }

        if len(summary_data['abstract']) > 100:
            summary_data['size'] = 4
        if len(summary_data['abstract']) > 250:
            summary_data['size'] = 5

        keyword = '<span class="label label-default">%s</span>\n'

        if ',' in summary_data['event_keywords']:
            sep = ','
        else:
            sep = ' '

        for word in summary_data['event_keywords'].split(sep):
            summary_data['keywords'] += keyword % word

        if ',' in summary_data['event_topics']:
            sep = ','
        else:
            sep = ' '

        for topic in summary_data['event_topics'].split(sep):
            summary_data['topics'] += keyword % topic

        summary_data['keywords'] = summary_data['keywords'].rstrip('\n')
        summary_data['topics'] = summary_data['topics'].rstrip('\n')

        if len(summary_data['author']) > 1:
            for speaker in summary_data['author']:
                summary_data['speakers'] += " " + speaker + ", "
            summary_data['speakers'] = summary_data['speakers'].rstrip(', ')
        elif len(summary_data['author']) == 1:
            summary_data['speakers'] = summary_data['author'][0]
        else:
            user = objectmodels['user'].find_one({'uuid': session.owner})
            summary_data['speakers'] = user.name

        summary = """<div class="event_summary">
            <h5> {speakers} - Type: {event_type}""".format(**summary_data)
        if len(summary_data['topics']) > 0:
            summary += " - <small>Topics: {topics}</small>".format(**summary_data)
        summary += """</h5>\n<h{size}>{abstract}</h{size}>
            <div class="row">
                <div class="col-md-10">
                    {keywords}
                </div>
                <div class="col-md-2">
                    <small>Talk ID: {event_id}</small>
                </div>
            </div>
        </div>
        """.format(**summary_data)

        initial = {
            'uuid': std_uuid(),
            'owner': event.user.uuid,
            'name': session.name,
            'calendar': calendar_uuid,
            'created': std_now(),
            'recurring': False,
            'duration': str(session_type.length),
            'category': 'session',
            'location': calendar.name,
            'summary': summary,
            'session': session.uuid
        }
        self.log(initial, pretty=True)
        session_event = objectmodels['event'](initial)

        session_event.save()

        notification = {
            'component': 'isomer.session.sessionmanager',
            'action': 'session_confirm',
            'data': {
                'uuid': session_uuid,
                'result': True
            }
        }

        self.fireEvent(send(event.client.uuid, notification))
