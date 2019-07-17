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
from tools import java_tools
import requests
from concurrent.futures import ThreadPoolExecutor


app = Flask(__name__)
log = logger.get_logger('main')
build_executor = BuildExecutor()
job_executor = ThreadPoolExecutor(10)

GIT_TMP_DIR = '/tmp/buildcenter/git'
COMPOSITION_TEMPLATE_NAME = 'CompositionTemplate'
COMPOSITION_TEMPLATE_GIT = 'git@192.168.1.104:SeptemberHX/compositiontemplate.git'

git_info = {
    'project_name': 'MFramework',
    'git_url': 'http://192.168.1.104:12345/mframework.git',
    'branch': 'test2',
    'main_class': 'com.septemberhx.sampleservice.MMain',
    'build_id': 'build_1',
    'module': 'SampleService'
}

test_build_info = BuildInfo(
    project_name='CompositionTemplate',
    git_url='git@192.168.1.104:SeptemberHX/compositiontemplate.git',
    git_tag='',
    docker_image_name='composition02',
    docker_image_tag='v1.0.1',
    docker_image_owner='192.168.1.104:5000/septemberhx',
    id='1',
    module_name='',
    branch='composition02'
)

composition_info = {
    'id': 'Composition_13123123123',
    'name': 'composition02',
    'docker_tag': 'v1.0.2',
    'docker_owner': '192.168.1.104:5000/septemberhx',
    'docker_name': 'composition01',
    'dependencies': [
        {
            'groupId': 'septemberhx',
            'artifactId': 'SampleService3',
            'version': '1.0-SNAPSHOT',
        },
    ],
    'chain_list': [
        {
            'className': "com.septemberhx.sampleservice3.controller.OtherController",
            'functionName': "wrapper"
        },
    ],
    'register_url': 'http://192.168.1.104:30761/eureka',
}

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
    try:
        parameter = {
            'jobId': build_id
        }
        data = urlencode(parameter)
        url = urljoin('http://{0}:{1}'.format(config.CLUSTER_CONFIG['server_ip'], config.CLUSTER_CONFIG['server_port']), config.CLUSTER_CONFIG['notify_path'])
        url = '{0}?{1}'.format(url, data)
        r = requests.get(url)
        log.info('Job {0} notified'.format(build_id))
        during_building_dict.pop(build_id)
    except Exception as e:
        log.error('Failed to notify server')
        log.error(e)


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


@app.route('/buildcenter/cbuild', methods=['POST'])
def accept_cbuild_job():
    data_json = json.loads(request.get_data())
    log.info('Accept job {0}: {1}'.format(data_json['id'], data_json))
    job_executor.submit(do_composition_job, data_json)
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
    repo, project_dir = clone_repo(git_info['project_name'], git_info['git_url'])
    create_or_checkout_branch(repo, git_info['branch'])

    # do the main stuff here
    process_project_files(project_dir, test_build_info)

    # commit the changes in the new branch
    commit_current_branch(repo, git_info['build_id'])


def clone_repo(project_name, git_url):
    if not os.path.exists(GIT_TMP_DIR) or not os.path.isdir(GIT_TMP_DIR):
        os.mkdir(GIT_TMP_DIR)
    project_dir = os.path.join(GIT_TMP_DIR, project_name)

    # clone the repo and checkout master branch
    try:
        if not os.path.exists(project_dir):
            repo = git.Repo.clone_from(url=git_url, to_path=project_dir)
        else:
            repo = git.Repo(project_dir)
        repo.git.checkout('master')
        return repo, project_dir
    except Exception as e:
        log.error('Failed to clone repo: {0}'.format(git_url))
        log.error(e)
        return None, None


def create_or_checkout_branch(repo, branch):
    # create a new branch from master
    try:
        if branch not in repo.heads:
            repo.git.branch(branch)
            repo.git.checkout(branch)
            repo.git.push('-u', 'origin', branch)
        else:
            repo.git.stash('save')
            repo.git.checkout(branch)
            repo.git.stash('save')
    except Exception as e:
        log.error('Failed to checkout branch {0}'.format(branch))
        log.error(e)


def commit_current_branch(repo, info):
    # commit the changes in the new branch
    try:
        repo.git.add(A=True)
        repo.git.commit('-m', info)
        repo.git.push()
    except Exception as e:
        log.error('Failed to commit and push')
        log.error(e)


def do_composition_job(composition_info):
    repo, project_dir = clone_repo(COMPOSITION_TEMPLATE_NAME, COMPOSITION_TEMPLATE_GIT)
    create_or_checkout_branch(repo, composition_info['name'])

    # create pom.
    with open(os.path.join(project_dir, 'pom.xml'), 'w') as pom_file:
        pom_file.write(java_tools.generate_pom_file(composition_info['dependencies']))

    # write controller
    with open(os.path.join(project_dir, 'src/main/java/com/septemberhx/mcomposition/', 'CompositionController.java'), 'w') as controller_file:
        controller_file.write(java_tools.generate_com_controller(composition_info['chain_list']))

    # write application.yaml
    with open(os.path.join(project_dir, 'src/main/resources/', 'application.yaml'), 'w') as yaml_file:
        yaml_file.write(java_tools.generate_application_yaml(composition_info['name'], composition_info['register_url']))

    # commit
    commit_current_branch(repo, composition_info['name'])

    # build
    build_info = BuildInfo(
        project_name=COMPOSITION_TEMPLATE_NAME,
        git_url=COMPOSITION_TEMPLATE_GIT,
        git_tag='',
        docker_image_name=composition_info['name'],
        docker_image_tag=composition_info['docker_tag'],
        docker_image_owner=composition_info['docker_owner'],
        id=composition_info['id'],
        module_name='',
        branch=composition_info['name']
    )
    build_job(build_info)


if __name__ == '__main__':
    build_test()
    app.run(host='0.0.0.0', port=54321)
    # process_build()
    # notify_job_finished('Build_c3961b6b-3963-4386-a7f4-f7098e680820')
    # do_composition_job()
