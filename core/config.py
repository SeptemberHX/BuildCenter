#!/usr/bin/env python3
# encoding: utf-8

"""
@File: config.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

JENKINS_CONFIG = {
    'username': 'SeptemberHX',
    'password': 'tianjianshan',
    'server': 'http://192.168.1.104:5002/',
    'notify_http_url': 'http://192.168.1.102:54321/buildcenter/notifyBuildJob',
    'credentials_id': '489a5191-b67d-4aad-943d-94dadf733aff',
    'new_cre_id': 'd6981ee6-132a-49b0-802a-cf3bdc76165b'
}

CLUSTER_CONFIG = {
    'server_ip': '192.168.1.104',
    'server_port': 8083,
    'notify_path': '/job/buildNotify',
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
