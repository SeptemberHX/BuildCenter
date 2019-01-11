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
from jenkinsapi.constants import *
from jenkinsapi.custom_exceptions import NoResults
from core import config, logger
from core.build_info import BuildInfo
from core.constant import *
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
        self.next_build_number = 1

    def create_job(self, build_info: BuildInfo):
        """
        create a job
        :param build_info:
        :return: next build number
        """
        if not JenkinsBuildProcess.J.has_job(build_info.project_name):
            with open('resource/jenkins_pipeline_config.xml') as f:
                lines = f.readlines()
            job_config = ''.join(lines).format(
                '{0}/{1}'.format(build_info.docker_image_owner, build_info.docker_image_name),
                build_info.git_url,
                build_info.docker_image_tag
            )
            self.job = JenkinsBuildProcess.J.create_job(build_info.project_name, job_config)
            JenkinsBuildProcess.log.debug('Job {0} created'.format(self.job.name))
        else:
            self.job = JenkinsBuildProcess.J.get_job(build_info.project_name)
            JenkinsBuildProcess.log.debug('Job {0} exists'.format(self.job.name))
        self.next_build_number = self.job.get_next_build_number()
        JenkinsBuildProcess.log.debug("Job {0}'s next build number is {0}".format(self.next_build_number))
        return self.next_build_number

    def run_job(self):
        if self.job is not None and self.check_if_build_finished(self.next_build_number - 1):
            JenkinsBuildProcess.J.build_job(self.job.name)
            JenkinsBuildProcess.log.debug(
                'Job {0} build #{1} started'.format(self.job.name, self.next_build_number))
            self.next_build_number = self.next_build_number + 1
            return True
        else:
            JenkinsBuildProcess.log.debug('Job is None or last build is not finished')
            return False

    def get_job_status(self):
        status = BUILD_UNKNOWN
        last_build = None
        try:
            last_build = self.job.get_build(self.next_build_number - 1)
        except NoResults as e:
            JenkinsBuildProcess.log.debug('NoResults exception happened')
            JenkinsBuildProcess.log.debug(e)
            status = BUILD_UNKNOWN
        except Exception as e2:
            JenkinsBuildProcess.log.error(e2)

        if last_build is not None:
            status = last_build.get_status()
            if status is None:
                status = BUILD_UNKNOWN
            elif status in [STATUS_SUCCESS]:
                status = BUILD_SUCCESS
            elif status in [STATUS_FAIL]:
                status = BUILD_FAIL
            JenkinsBuildProcess.log.debug("Job {0}'s build #{1} {2}".format(self.job.name, last_build.buildno, status))
        return status

    def check_if_build_finished(self, build_number):
        if self.job is not None:
            if build_number == 0:
                return True

            curr_job = self.job.get_build(build_number)
            JenkinsBuildProcess.log.debug(
                "Job {0}'s build #{1}'s state is {2}".format(self.job.name, build_number, curr_job.get_status()))
            if curr_job is not None and \
                    curr_job.get_status() in [STATUS_SUCCESS, STATUS_FAIL, RESULTSTATUS_FAILED, RESULTSTATUS_FAILURE]:
                return True
            elif curr_job is None:
                return True
        return False
