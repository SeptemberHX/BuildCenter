#!/usr/bin/env python3
# encoding: utf-8

"""
@File: logger.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

import logging

formatter = logging.Formatter('[%(asctime)s] [ %(filename)s:%(lineno)s ] [ %(levelname)s ] : %(message)s')
logger_file_handler = logging.FileHandler('./log.log')
logger_terminal_handler = logging.StreamHandler()
logger_file_handler.setFormatter(formatter)
logger_terminal_handler.setFormatter(formatter)


def get_logger(name, level=logging.DEBUG):
    """
    :param name:
    :param level:
    :return:
    :rtype: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(logger_file_handler)
    logger.addHandler(logger_terminal_handler)
    return logger
