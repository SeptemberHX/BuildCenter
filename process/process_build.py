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
    """
    Build given project with given build processor
    """
    def __init__(self, build_process: BaseBuildProcess):
        self.build_process = build_process

    def create_job(self, build_info: BuildInfo):
        """
        create a job for given build info
        :param build_info:
        :return:
        """
        return self.build_process.create_job(build_info)

    def run_job(self):
        """
        run a build for the job
        :return: whether project build was triggered
        """
        return self.build_process.run_job()

    def get_job_status(self):
        """
        get last build status
        :return:
        """
        return self.build_process.get_job_status()

    def finish_job(self, job_id: str):
        return self.build_process.finish_job(job_id)
