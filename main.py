#!/usr/bin/env python3
# encoding: utf-8

"""
@File: main.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

from process.process_build import BuildProcess
from process.build_process.jenkins_build_process import JenkinsBuildProcess
from core.build_info import BuildInfo

if __name__ == '__main__':
    test_build_info = BuildInfo(
        project_name='test_build_2',
        git_url='https://github.com/gustavoapolinario/microservices-node-example-todo-frontend.git',
        git_tag='',
        docker_image_name='docker-test',
        docker_image_tag='v3',
        docker_image_owner='septemberhx',
    )
    build_process = BuildProcess(JenkinsBuildProcess())
    build_process.create_job(test_build_info)
    build_process.run_job()
    build_process.get_job_status()
