#!/usr/bin/env python3
# encoding: utf-8

"""
@File: process_build.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

from process.build_process.base_build_process import BaseBuildProcess
from core.build_info import BuildInfo


class BuildProcess:
    def __init__(self, build_process: BaseBuildProcess):
        self.build_process = build_process

    def create_job(self, build_info: BuildInfo):
        self.build_process.create_job(build_info)

    def run_job(self):
        self.build_process.run_job()

    def get_job_status(self):
        self.build_process.get_job_status()
