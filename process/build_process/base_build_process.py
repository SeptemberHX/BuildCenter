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
    """
    Base class for all build processor
    """
    def create_job(self, build_info: BuildInfo):
        pass

    def run_job(self):
        pass

    def get_job_status(self):
        pass

    def finish_job(self, job_id: str):
        pass
