# -*- coding: utf-8 -*-

import pika
import os


class Config(object):

    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 5672

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port

    def to_connection_params(self):
        return pika.ConnectionParameters(self.host, self.port)


def new_default_config():
    host = os.environ.get('XIVO_BUS_HOST', Config.DEFAULT_HOST)
    port = int(os.environ.get('XIVO_BUS_PORT', Config.DEFAULT_PORT))
    return Config(host, port)


default_config = new_default_config()
