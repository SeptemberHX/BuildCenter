#!/usr/bin/env python3
# encoding: utf-8

"""
@File: main.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

from executor.build_executor import BuildExecutor
from core.build_info import BuildInfo
from flask import Flask, request
import json
from core import logger
import git
import os
from tools import pom_tools

app = Flask(__name__)
log = logger.get_logger('main')
build_executor = BuildExecutor()

GIT_TMP_DIR = '/tmp/buildcenter/git'

git_info = {
    'project_name': 'MFramework',
    'git_url': 'http://192.168.1.104:12345/mframework.git',
    'branch': 'test2',
    'main_class': 'com.septemberhx.sampleservice.MMain',
    'build_id': 'build_1',
    'module': 'SampleService'
}

test_build_info = BuildInfo(
    project_name='MFramework',
    git_url='git@192.168.1.104:SeptemberHX/mframework.git',
    git_tag='',
    docker_image_name='sampleservice',
    docker_image_tag='v1.3',
    docker_image_owner='192.168.1.104:5000/septemberhx',
    class_name='com.septemberhx.sampleservice.controller.PeterController',
    url='/peter',
    id='1',
    module_name='SampleService',
    branch='test2'
)


def build_test():
    build_executor.execute(test_build_info)


@app.route("/buildcenter/notifyBuildJob", methods=['GET', 'POST'])
def jenkins_message_receiver():
    data = request.get_data()
    data_json = json.loads(data)
    log.info(data_json)
    return 'Received'


@app.route("/buildcenter/buildjob", methods=['POST'])
def start_build_job():
    job_info = json.loads(request.get_data())
    log.info('Job received: {0}'.format(job_info))
    build_info = BuildInfo(job_info['projectName'], job_info['gitUrl'], job_info['gitTag'], job_info['imageName'],
                           job_info['imageTag'], job_info['imageOwner'], job_info['id'])
    build_executor.execute(build_info)
    return 'Received'


@app.route("/hello")
def hello():
    return "Hello, world!"


def process_project_files(src_dir: str, build_info: BuildInfo):
    module_name = git_info['module']
    # modify pom.xml
    if module_name:
        pom_file_path = os.path.join(src_dir, module_name, 'pom.xml')
    else:
        pom_file_path = os.path.join(src_dir, 'pom.xml')
    pom_file = pom_tools.PomTools(pom_file_path)
    main_class_name = pom_file.get_main_class()[0]  # type: str

    pom_file.change_main_class(git_info['main_class'])
    pom_file.save_to_file(pom_file_path)

    # add MController.java and MMain.java to src
    package_name = '.'.join(main_class_name.split('.')[:-1])
    if module_name:
        main_file_dir = os.path.join(src_dir, module_name, 'src/main/java', *package_name.split('.'))
    else:
        main_file_dir = os.path.join(src_dir, 'src/main/java', *package_name.split('.'))
    log.info('Raw main class: {0}'.format(main_class_name))
    log.info('Package: {0}'.format(package_name))
    log.info('Main src dir: {0}'.format(main_file_dir))

    with open('resource/MController.java') as f:
        lines = f.readlines()
        content = ''.join(lines).format(
            package_name=package_name,
            mobject_class=build_info.class_name,
            url_values='"/{0}"'.format(build_info.url),
        )
        with open(os.path.join(main_file_dir, 'MController.java'), 'w') as fo:
            fo.write(content)
    with open('resource/MMain.java') as f:
        lines = f.readlines()
        content = ''.join(lines).format(
            package_name=package_name,
        )
        with open(os.path.join(main_file_dir, 'MMain.java'), 'w') as fo:
            fo.write(content)


def process_build():
    if not os.path.exists(GIT_TMP_DIR) or not os.path.isdir(GIT_TMP_DIR):
        os.mkdir(GIT_TMP_DIR)
    project_dir = os.path.join(GIT_TMP_DIR, git_info['project_name'])

    # clone the repo and checkout master branch
    try:
        if not os.path.exists(project_dir):
            repo = git.Repo.clone_from(url=git_info['git_url'], to_path=project_dir)
        else:
            repo = git.Repo(project_dir)
        repo.git.checkout('master')
    except Exception as e:
        log.error('Failed to clone repo: {0}'.format(git_info['git_url']))
        log.error(e)
        return False

    # create a new branch from master
    try:
        if git_info['branch'] not in repo.heads:
            repo.git.branch(git_info['branch'])
            repo.git.checkout(git_info['branch'])
            repo.git.push('-u', 'origin', git_info['branch'])
        else:
            repo.git.checkout(git_info['branch'])
            repo.git.stash('save')
    except Exception as e:
        log.error('Failed to checkout branch {0}'.format(git_info['branch']))
        log.error(e)
        return False

    # do the main stuff here
    process_project_files(project_dir, test_build_info)

    # commit the changes in the new branch
    try:
        repo.git.add(A=True)
        repo.git.commit('-m', git_info['build_id'])
        repo.git.push()
    except Exception as e:
        log.error('Failed to commit and push')
        log.error(e)


if __name__ == '__main__':
    build_test()
    app.run(host='0.0.0.0', port=54321)
    # process_build()
