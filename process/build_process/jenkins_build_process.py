#!/usr/bin/env python3
# encoding: utf-8

"""
@File: jenkins_build_process.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.job import Job
from jenkinsapi.custom_exceptions import NoResults
from core import config, logger
from core.build_info import BuildInfo
from process.build_process import base_build_process


class JenkinsBuildProcess(base_build_process.BaseBuildProcess):
    """
    Jenkins build support. It will use jenkins to build your project
    """
    J = None  # type: Jenkins
    log = logger.get_logger('JenkinsBuildProcess')

    def __init__(self):
        if JenkinsBuildProcess.J is None:
            JenkinsBuildProcess.J = Jenkins(
                baseurl=config.JENKINS_CONFIG['server'],
                username=config.JENKINS_CONFIG['username'],
                password=config.JENKINS_CONFIG['password'],
            )
            JenkinsBuildProcess.log.debug('Jenkins version: {0}'.format(JenkinsBuildProcess.J.version))
        self.job = None  # type: Job

    def create_job(self, build_info: BuildInfo):
        if not JenkinsBuildProcess.J.has_job(build_info.project_name):
            with open('resource/jenkins_pipeline_config.xml') as f:
                lines = f.readlines()
            job_config = ''.join(lines).format(
                build_info.docker_image_owner,
                build_info.git_url,
                build_info.docker_image_tag
            )
            self.job = JenkinsBuildProcess.J.create_job(build_info.project_name, job_config)
            JenkinsBuildProcess.log.debug('Job {0} created'.format(self.job.name))
        else:
            self.job = JenkinsBuildProcess.J.get_job(build_info.project_name)
            JenkinsBuildProcess.log.debug('Job exists')

    def run_job(self):
        if self.job:
            JenkinsBuildProcess.J.build_job(self.job.name)
            JenkinsBuildProcess.log.debug(
                '{0} build #{1} started'.format(self.job.name, self.job.get_next_build_number()))
            return True
        else:
            JenkinsBuildProcess.log.debug('Job is None')
            return False

    def get_job_status(self):
        status = None
        last_build = None
        try:
            last_build = self.job.get_last_build()
        except NoResults as e:
            JenkinsBuildProcess.log.debug('NoResults exception happened')
            status = 'NOT_KNOW'
        except Exception as e2:
            JenkinsBuildProcess.log.error(e2)

        if last_build:
            status = last_build.get_status()
            if status is None:
                status = 'NOT_KNOW'
        JenkinsBuildProcess.log.debug('Build {0}'.format(status))
        return status
