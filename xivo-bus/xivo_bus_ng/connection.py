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

    # XXX c'est un peu inutile ces abstractions là

    def basic_cancel(self, consumer_tag):
        return self._chan.basic_cancel(consumer_tag=consumer_tag)

    def basic_consume(self, callback, queue_name, no_ack):
        return self._chan.basic_consume(callback, queue_name, no_ack)

    def basic_publish(self, exchange_name, routing_key, body):
        return self._chan.basic_publish(exchange_name, routing_key, body)

    def exchange_declare(self, exchange_name, exchange_type, durable):
        return self._chan.exchange_declare(exchange=exchange_name, type=exchange_type, durable=durable)

    def queue_declare(self, queue_name, durable, exclusive=False):
        return self._chan.queue_declare(queue=queue_name, durable=durable, exclusive=exclusive)

    def queue_bind(self):
        pass

    def start_consuming(self):
        self._chan.start_consuming()
