# -*- coding: utf-8 -*-

import pika
from xivo_bus_ng.config import default_config


class Connection(object):

    # XXX small layer over pika/BlockingConnection
    #     + handling of reconnection and something
    # XXX should be able to another type of connection (SelectConnection?)

    def __init__(self, config=None):
        if config is None:
            config = default_config
        self._config = config
        self._conn = None
        self._chan = None

    def connect(self):
        if self._conn is not None:
            raise Exception('already connected')

        self._conn = pika.BlockingConnection(self._config.to_connection_params())
        self._chan = self._conn.channel()

    def close(self):
        if self._conn is None:
            return

        self._conn.close()
        self._conn = None
        self._chan = None

    def basic_publish(self, exchange, routing_key, body):
        self._chan.basic_publish(exchange, routing_key, body)

    def exchange_declare(self, exchange, type_, durable):
        self._chan.exchange_declare(exchange=exchange, type=type_, durable=durable)

    def queue_declare(self):
        pass

    def queue_bind(self):
        pass
