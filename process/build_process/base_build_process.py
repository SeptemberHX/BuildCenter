#!/usr/bin/env python3
# encoding: utf-8

"""
@File: base_build_process.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

from core.build_info import BuildInfo


class BaseBuildProcess:
    def create_job(self, build_info: BuildInfo):
        pass

    def run_job(self):
        pass

    def get_job_status(self):
        pass
