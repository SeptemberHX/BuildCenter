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
from flask import Flask

app = Flask(__name__)


def build_test():
    test_build_info = BuildInfo(
        project_name='docker_java_test3',
        git_url='https://github.com/SeptemberHX/java-docker-build-tutorial.git',
        git_tag='',
        docker_image_name='docker_java_test',
        docker_image_tag='v1',
        docker_image_owner='192.168.1.104:5000/septemberhx',
    )
    build_executor = BuildExecutor()
    build_executor.execute(test_build_info)


@app.route("/hello")
def hello():
    return "Hello, world!"


if __name__ == '__main__':
    # app.run(port=54321)
    build_test()