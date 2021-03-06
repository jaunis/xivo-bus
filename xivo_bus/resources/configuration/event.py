# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class ConfigurationEvent(ResourceConfigEvent):

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['live_reload_enabled'])


class LiveRealoadEditedEvent(ConfigurationEvent):
    name = 'live_reload_edited'

    def __init__(self, live_reload_enabled):
        self.live_reload_enabled = live_reload_enabled

    def marshal(self):
        return {
            'live_reload_enabled': self.live_reload_enabled
        }
