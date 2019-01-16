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


if __name__ == '__main__':
    test_build_info = BuildInfo(
        project_name='docker_java_test',
        git_url='https://github.com/SeptemberHX/java-docker-build-tutorial.git',
        git_tag='',
        docker_image_name='docker_java_test',
        docker_image_tag='v1',
        docker_image_owner='septemberhx',
    )
    build_executor = BuildExecutor()
    build_executor.execute(test_build_info)
