# -*- coding: utf-8 -*-

from xivo_bus_ng import entity
from xivo_bus_ng.marshal import marshal


class Event(object):

    def marshal(self):
        return marshal(self)


class CallFormResultEvent(Event):

    name = 'call_form_result'
    exchange = entity.xivo_cti_exchange

    def __init__(self, user_id, variables):
        self.user_id = user_id
        self.variables = variables

    def publish(self, connection):
        connection.basic_publish(self.exchange.name, self.name, self.marshal())

    def marshal(self):
        # XXX name is ugly
        return {
            'user_id': self.user_id,
            'variables': self.variables,
        }
