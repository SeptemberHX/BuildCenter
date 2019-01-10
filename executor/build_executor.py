#!/usr/bin/env python3
# encoding: utf-8

"""
@File: build_executor.py
@Author: septemberhx
@Date: 2019-01-09
@Version: 0.01
"""

from core.build_info import BuildInfo
from process.process_build import BuildProcess
from process.build_process.jenkins_build_process import JenkinsBuildProcess


class BuildExecutor:

    def __init__(self):
        self.build_process = BuildProcess(JenkinsBuildProcess())

    def execute(self, build_info: BuildInfo):
        pass
