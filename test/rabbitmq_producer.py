#!/usr/bin/env python3
# encoding: utf-8

"""
@File   : rabbitmq_producer.py
@Author : septemberhx
@Date   : 2019-01-11
@Version: 0.01
"""


from core.config import RABBITMQ_CONFIG
import threading
import pika
import time


class RabbitMQProducer:

    def __init__(self):
        self.credentials = pika.PlainCredentials(RABBITMQ_CONFIG['username'], RABBITMQ_CONFIG['password'])
        self.connection = None
        self.channel = None  # type: pika.adapters.blocking_connection.BlockingChannel
        self.reply_queue = None
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
        self.reply_queue = self.channel.queue_declare(RABBITMQ_CONFIG['reply_queue_name'])

    def execute(self):
        response_thread = threading.Thread(target=self.get_response)
        response_thread.start()

        for i in range(0, 10):
            self.channel.basic_publish(exchange='',
                                       routing_key=RABBITMQ_CONFIG['consume_queue_name'],
                                       properties=pika.BasicProperties(reply_to=self.reply_queue.method.queue, message_id='{0}'.format(i)),
                                       body='Hello World!')
            time.sleep(3)

    def get_response(self):
        self.channel.basic_consume(self.on_response, self.reply_queue.method.queue, no_ack=False)
        self.channel.start_consuming()

    def on_response(self, ch, method, props, body):
        print(props.message_id, body)


if __name__ == '__main__':
    e = RabbitMQProducer()
    e.execute()
