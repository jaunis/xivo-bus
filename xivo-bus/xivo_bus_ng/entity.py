# -*- coding: utf-8 -*-

class Exchange(object):

    def __init__(self, name, type_, durable):
        self.name = name
        self.type = type_
        self.durable = durable

    def declare(self, connection):
        connection.exchange_declare(self.name, self.type, self.durable)


class Queue(object):

    def __init__(self, name, durable):
        self.name = name
        self.durable = durable

    def declare(self, connection):
        connection.queue_declare(self.name, self.durable)


class Binding(object):
    # XXX maybe not that useful

    def __init__(self, exchange_name, queue_name):
        pass

# XXX could be in their own module "entity.exchange"
xivo_cti_exchange = Exchange('xivo-cti', 'direct', True)
xivo_exchange = Exchange('xivo', 'fanout', False)

# XXX could be in their own module "entity.queues"
xivo_agent_queue = Queue('xivo-agent', False)
