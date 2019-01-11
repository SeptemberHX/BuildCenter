#!/usr/bin/env python3
# encoding: utf-8

"""
@File: main.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

from executor.build_executor import BuildExecutor
from core.build_info import BuildInfo
from core.logger import get_logger


if __name__ == '__main__':
    test_build_info = BuildInfo(
        project_name='test_build_2',
        git_url='https://github.com/gustavoapolinario/microservices-node-example-todo-frontend.git',
        git_tag='',
        docker_image_name='docker-test',
        docker_image_tag='v3',
        docker_image_owner='septemberhx',
    )
    # build_executor = BuildExecutor()
    # build_executor.execute(test_build_info)
    logger = get_logger('main')
    logger.info('Info')
    logger.debug('Debug')
    logger.critical('Critical')
