#!/usr/bin/env python3
# encoding: utf-8

"""
@File: main.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""
from urllib.parse import urlencode, urljoin

from executor.build_executor import BuildExecutor
from core.build_info import BuildInfo
from core import config
from flask import Flask, request
import json
from core import logger
import git
import os
from tools import pom_tools
import requests

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
    docker_image_name='sampleservice1',
    docker_image_tag='v1.0.1',
    docker_image_owner='192.168.1.104:5000/septemberhx',
    id='1',
    module_name='SampleService1',
    branch='master'
)

during_building_dict = {}  # type: dict[str, BuildInfo]


def build_test():
    build_executor.execute(test_build_info)


@app.route("/buildcenter/notifyBuildJob", methods=['GET', 'POST'])
def jenkins_message_receiver():
    data = request.get_data()
    data_json = json.loads(data)
    log.info('Receive build result: {0}'.format(data_json))
    if 'buildId' in data_json:
        log.info('Build job finished: {0}'.format(data_json['buildId']))
        notify_job_finished(data_json['buildId'])
    return 'Received'


def build_job(build_info: BuildInfo):
    log.info('Start to build {0}: {1}'.format(build_info.id, build_info))
    during_building_dict[build_info.id] = build_info
    build_executor.execute(build_info)


def notify_job_finished(build_id: str):
    parameter = {
        'jobId': build_id
    }
    data = urlencode(parameter)
    url = urljoin('http://{0}:{1}'.format(config.CLUSTER_CONFIG['server_ip'], config.CLUSTER_CONFIG['server_port']), config.CLUSTER_CONFIG['notify_path'])
    url = '{0}?{1}'.format(url, data)
    r = requests.get(url)
    log.info('Job {0} notified'.format(build_id))
    during_building_dict.pop(build_id)


@app.route("/buildcenter/build", methods=['POST'])
def accept_build_job():
    data_json = json.loads(request.get_data())
    log.info('Accept job {0}: {1}'.format(data_json['id'], data_json))
    build_info = BuildInfo(
        project_name=data_json['projectName'],
        module_name=data_json['moduleName'],
        git_url=data_json['gitUrl'],
        git_tag=data_json['gitTag'],
        docker_image_name=data_json['imageName'],
        docker_image_tag=data_json['imageTag'],
        docker_image_owner=data_json['imageOwner'],
        id=data_json['id'],
        branch=data_json['branch']
    )
    build_job(build_info)
    return "Accepted"


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
    # build_test()
    app.run(host='0.0.0.0', port=54321)
    # process_build()
    # notify_job_finished('Build_c3961b6b-3963-4386-a7f4-f7098e680820')
