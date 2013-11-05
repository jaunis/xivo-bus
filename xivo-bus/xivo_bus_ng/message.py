# -*- coding: utf-8 -*-

import json
from xivo_bus_ng import entity


class Event(object):

    def marshal(self):
        return json.dumps({'name': self.name, 'data': self._to_data()})

    def _to_data(self):
        # to be overriden in derived class
        return None


class CallFormResultEvent(Event):

    name = 'call_form_result'
    exchange = entity.xivo_cti_exchange

    def __init__(self, user_id, variables):
        self.user_id = user_id
        self.variables = variables

    def publish(self, connection):
        connection.basic_publish(self.exchange.name, self.name, self.marshal())

    def _to_data(self):
        # XXX name is ugly
        return {
            'user_id': self.user_id,
            'variables': self.variables,
        }
