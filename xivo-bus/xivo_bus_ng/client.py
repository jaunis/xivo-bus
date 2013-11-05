# -*- coding: utf-8 -*-

class Client(object):

    def __init__(self, connection):
        self._connection = connection

    def declare(self, entity):
        entity.declare(self._connection)

    def publish(self, message):
        message.publish(self._connection)

    def rpc_call(self, rpc_message):
        # TODO
        pass
