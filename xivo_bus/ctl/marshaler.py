# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
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

import json
from xivo_bus.ctl.response import CommandResponse


class Marshaler(object):

    def __init__(self, commands_registry=None):
        self._commands_registry = commands_registry

    def marshal_command(self, command):
        return json.dumps({'name': command.name, 'data': command.marshal()})

    def marshal_response(self, response):
        return json.dumps(response.marshal())

    def unmarshal_command(self, data):
        msg = self.unmarshal_message(data)
        msg_name = msg['name']
        msg_cmd = msg['data']
        cmd_class = self._commands_registry[msg_name]
        return cmd_class.unmarshal(msg_cmd)

    def unmarshal_response(self, data):
        msg = self.unmarshal_message(data)
        return CommandResponse.unmarshal(msg)

    def unmarshal_message(self, data):
        return json.loads(data)
