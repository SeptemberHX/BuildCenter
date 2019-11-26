#!/usr/bin/env python3
# encoding: utf-8

"""
@File: rabbitmq_executor.py
@Author: septemberhx
@Date: 2019-01-10
@Version: 0.01
"""

from core.config import RABBITMQ_CONFIG
from core.logger import get_logger
from executor.command_executor import CommandExecutor
import pika
import threading


class RabbitMQExecutor:

    logger = get_logger('RabbitMQExecutor')

    def __init__(self):
        self.credentials = pika.PlainCredentials(RABBITMQ_CONFIG['username'], RABBITMQ_CONFIG['password'])
        self.connection = None
        self.channel = None  # type: pika.adapters.blocking_connection.BlockingChannel
        self.connect_to_rabbitmq()

    def connect_to_rabbitmq(self):
        if self.connection is not None:
            self.connection.close()
            self.channel.close()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            RABBITMQ_CONFIG['ip'],
            RABBITMQ_CONFIG['port'],
            RABBITMQ_CONFIG['path'],
            self.credentials
        ))
        self.channel = self.connection.channel()
        self.channel.queue_declare(RABBITMQ_CONFIG['consume_queue_name'])

    def execute(self):
        self.channel.basic_consume(self.process_thread, queue=RABBITMQ_CONFIG['consume_queue_name'])
        self.channel.start_consuming()

    def process(self, ch, method, properties, body):
        """
        callback function for channel event consuming.
        It will publish reply message to given queue in properties.reply_to
        All messages are json style
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        command_executor = CommandExecutor()
        result = command_executor.process(body)
        self.channel.basic_publish(exchange='',
                                   routing_key=properties.reply_to,
                                   properties=pika.BasicProperties(message_id=properties.message_id),
                                   body=result)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)
        RabbitMQExecutor.logger.debug('Reply published')

    def process_thread(self, ch, method, properties, body):
        """
        Execute self.process in a separate thread
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        RabbitMQExecutor.logger.debug('Receive event: {0}'.format(properties.message_id))
        t = threading.Thread(target=self.process, args=(ch, method, properties, body,))
        t.start()


if __name__ == '__main__':
    executor = RabbitMQExecutor()
    executor.execute()
