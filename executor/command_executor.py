#!/usr/bin/env python3
# encoding: utf-8

"""
@File    : command_executor
@Author  : septemberhx
@Date    : 2019-01-16
@Version : 0.01
"""

from time import sleep
from core.logger import get_logger


class CommandExecutor:

    logger = get_logger('CommandExecutor')

    def __init__(self):
        pass

    def process(self, command_json_str: str):
        """
        process command
        :param command_json_str:
        :return: str
        """
        sleep(5)
        CommandExecutor.logger.debug('Command Process complete')
        return ''
