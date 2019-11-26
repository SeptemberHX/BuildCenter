#!/usr/bin/env python3
# encoding: utf-8

"""
@File: jenkins_build_process.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

from jenkins import Jenkins, NotFoundException
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
                url=config.JENKINS_CONFIG['server'],
                username=config.JENKINS_CONFIG['username'],
                password=config.JENKINS_CONFIG['password'],
            )
            JenkinsBuildProcess.log.debug(JenkinsBuildProcess.J.get_whoami())
            JenkinsBuildProcess.log.debug('Jenkins version: {0}'.format(JenkinsBuildProcess.J.get_version()))
        self.job_info_dict = {}

    def create_job(self, build_info: BuildInfo):
        """
        create a job
        :param build_info:
        """
        self.job_info_dict[build_info.id] = build_info

        # The job will be refreshed whether it is existed or not
        with open('resource/jenkins_pipeline_config.xml') as f:
            lines = f.readlines()
            module_option = ''
            docker_dir = '.'
            if build_info.module_name and len(build_info.module_name) != 0:
                module_option = '-pl {0} -am'.format(build_info.module_name)
                docker_dir = build_info.module_name
            job_config = ''.join(lines).format(
                gitUrl=build_info.git_url,
                imageTag='{0}/{1}:{2}'.format(
                    build_info.docker_image_owner, build_info.docker_image_name, build_info.docker_image_tag),
                notifyHttpUrl=config.JENKINS_CONFIG['notify_http_url'],
                module_name=build_info.module_name,
                credentialsId=config.JENKINS_CONFIG['credentials_id'],
                branch=build_info.branch,
                build_id=build_info.id,
                module_option=module_option,
                docker_dir=docker_dir
            )

            if JenkinsBuildProcess.J.job_exists(build_info.project_name):
                JenkinsBuildProcess.J.reconfig_job(build_info.project_name, job_config)
                JenkinsBuildProcess.log.debug('Job {0} exists, reconfig it'.format(build_info.project_name))
            else:
                JenkinsBuildProcess.J.create_job(build_info.project_name, job_config)
                JenkinsBuildProcess.log.debug('Job {0} created'.format(build_info.project_name))

            # Get the build number of current build job
            build_number = 1
            job = JenkinsBuildProcess.J.get_job_info(build_info.project_name)
            if job:
                build_number = job['nextBuildNumber']
            JenkinsBuildProcess.J.build_job(build_info.project_name)
            JenkinsBuildProcess.log.debug('Job {0} build #{1} started'.format(build_info.project_name, build_number))

    def finish_job(self, job_id: str):
        if job_id in self.job_info_dict:
            self.job_info_dict.pop(job_id)
            JenkinsBuildProcess.log.info('Job {0} marked as finished'.format(job_id))

    def get_job_status(self):
        status = BUILD_UNKNOWN
        last_build = None
        try:
            last_build = self.job.get_build(self.next_build_number - 1)
        except NotFoundException as e:
            JenkinsBuildProcess.log.debug('NoResults exception happened')
            JenkinsBuildProcess.log.debug(e)
            status = BUILD_UNKNOWN
        except Exception as e2:
            JenkinsBuildProcess.log.error(e2)

        if last_build is not None:
            status = last_build.get_status()
            if status is None:
                status = BUILD_UNKNOWN
            JenkinsBuildProcess.log.debug("Job {0}'s build #{1} {2}".format(self.job.name, last_build.buildno, status))
        return status

    def check_if_build_finished(self, build_number):
        if self.job is not None:
            if build_number == 0:
                return True

            curr_job = self.job.get_build(build_number)
            JenkinsBuildProcess.log.debug(
                "Job {0}'s build #{1}'s state is {2}".format(self.job.name, build_number, curr_job.get_status()))
            if curr_job is not None:
                return True
            elif curr_job is None:
                return True
        return False
