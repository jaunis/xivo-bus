# -*- coding: utf-8 -*-

from xivo_bus_ng.marshal import unmarshal


class Client(object):

    def __init__(self, connection):
        self._connection = connection

    def declare(self, entity):
        entity.declare(self._connection)

    def new_consumer(self, queue, no_ack):
        consumer = _Consumer(self._connection)
        consumer.consume(queue, no_ack)
        return consumer

    def publish(self, message):
        message.publish(self._connection)

    def rpc_call(self, rpc_message):
        # TODO
        pass

    def start_consuming(self):
        self._connection.start_consuming()


class _Consumer(object):

    def __init__(self, connection):
        self._connection = connection
        self._consumer_tags = []
        self._msgs_registry = {}
        self._msgs_callback = {}

    def add_callback(self, message, callback):
        # FIXME name is bad
        if message.name in self._msgs_registry:
            raise Exception('callback already registered for %s' % message.name)
        self._msgs_registry[message.name] = message
        self._msgs_callback[message.name] = callback

    def consume(self, queue, no_ack):
        consumer_tag = self._connection.basic_consume(self._on_consume, queue.name, no_ack)
        self._consumer_tags.append(consumer_tag)

    def close(self):
        for consumer_tag in self._consumer_tags:
            self._connection.basic_cancel(consumer_tag=consumer_tag)
        self._consumer_tags = []

    def _on_consume(self, ch, method, props, body):
        # TODO error handling (see BusCtlServer)
        msg = unmarshal(self._msgs_registry, body)
        callback = self._msgs_callback[msg.name]

        # XXX hum, it does not cut it, can't call basic_ack from the callback
        #     arguments are ugly too, ...
        # XXX should take a "message" (message, client, method, props) and it
        #     could receive a "response" to send, and do the basic_ack by itself
        callback(msg, method, props)
