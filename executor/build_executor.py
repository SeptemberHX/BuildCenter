#!/usr/bin/env python3
# encoding: utf-8

"""
@File: build_executor.py
@Author: septemberhx
@Date: 2019-01-09
@Version: 0.01
"""

import time
from core.build_info import BuildInfo
from core.constant import *
from core.logger import get_logger
from process.process_build import BuildProcess
from process.build_process.jenkins_build_process import JenkinsBuildProcess


class BuildExecutor:

    logger = get_logger('BuildExecutor')

    def __init__(self):
        self.build_process = BuildProcess(JenkinsBuildProcess())

    def execute(self, build_info: BuildInfo):
        self.build_process.create_job(build_info)
        self.build_process.run_job()

        build_status = self.build_process.get_job_status()
        while build_status == BUILD_UNKNOWN:
            BuildExecutor.logger.debug('Task {0}#{1} not finished yet'.format(build_info.project_name, build_status))
            time.sleep(30)
            build_status = self.build_process.get_job_status()
        BuildExecutor.logger.debug('Task {0} finished with status {1}'.format(build_info.project_name, build_status))
        return build_status
