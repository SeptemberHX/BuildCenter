#!/usr/bin/env python3
# encoding: utf-8

"""
@File: build_info.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""


class BuildInfo:
    def __init__(self, project_name, git_url, git_tag, docker_image_name, docker_image_tag, docker_image_owner, id, module_name, branch):
        self.project_name = project_name
        self.git_url = git_url
        self.git_tag = git_tag
        self.docker_image_name = docker_image_name
        self.docker_image_tag = docker_image_tag
        self.docker_image_owner = docker_image_owner
        self.id = id  # str
        self.module_name = module_name
        self.branch = branch
