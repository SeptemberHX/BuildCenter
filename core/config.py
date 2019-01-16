#!/usr/bin/env python3
# encoding: utf-8

"""
@File: config.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

JENKINS_CONFIG = {
    'username': 'septemberhx',
    'password': 'tianjianshan',
    'server': 'http://107.191.56.183:8087/',
}

RABBITMQ_CONFIG = {
    'username': 'admin',
    'password': 'tianjianshan',
    'ip': '60.205.188.102',
    'port': 5672,
    'path': '/',
    'consume_queue_name': 'tasks',
    'reply_queue_name': 'replies',
}
