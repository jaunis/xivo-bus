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

import logging
from xivo_bus.ctl.amqp_transport_server import AMQPTransportServer
from xivo_bus.ctl.response import CommandResponse
from xivo_bus.ctl.marshaler import Marshaler
from xivo_bus.resources.agent import error
from xivo_bus.ctl.exception import BusCtlServerError

logger = logging.getLogger(__name__)


class BusCtlServer(object):

    _QUEUE_NAME = 'xivo'

    def __init__(self):
        self._transport = self._setup_transport()
        self._marshaler = None
        self._commands_registry = {}
        self._commands_callback = {}

    def _setup_transport(self):
        transport = AMQPTransportServer.create_and_connect(self._process_next_command,
                                                           self._QUEUE_NAME)
        return transport

    def add_command(self, cmd_class, callback):
        if cmd_class.name in self._commands_registry:
            raise Exception('command %r is already registered' % cmd_class.name)

        self._commands_registry[cmd_class.name] = cmd_class
        self._commands_callback[cmd_class.name] = callback

    def _process_next_command(self, request):
        response = CommandResponse()
        try:
            command = self._marshaler.unmarshal_command(request)
            callback = self._commands_callback[command.name]
            response.value = self._call_callback(callback, command)
        except BusCtlServerError as e:
            response.error = e.error
        except Exception:
            logger.error('Error while processing command', exc_info=True)
            response.error = error.SERVER_ERROR

        return self._reply_response(response)

    def _call_callback(self, callback, command):
        return callback(command)

    def _reply_response(self, response):
        return self._marshaler.marshal_response(response)

    def run(self):
        self._marshaler = Marshaler(self._commands_registry)
        self._transport.run()

    def close(self):
        self._transport.close()
        self._transport = None
