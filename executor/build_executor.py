#!/usr/bin/env python3
# encoding: utf-8

"""
@File: build_executor.py
@Author: septemberhx
@Date: 2019-01-09
@Version: 0.01
"""

from core.build_info import BuildInfo
from core.logger import get_logger
from process.process_build import BuildProcess
from process.build_process.jenkins_build_process import JenkinsBuildProcess


class BuildExecutor:

    logger = get_logger('BuildExecutor')

    def __init__(self):
        self.build_process = BuildProcess(JenkinsBuildProcess())

    def execute(self, build_info: BuildInfo):
        self.build_process.create_job(build_info)

    def finish(self, job_id: str):
        self.build_process.finish_job(job_id)
