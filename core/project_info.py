#!/usr/bin/env python3
# encoding: utf-8

"""
@File: project_info.py
@Author: septemberhx
@Date: 2018-12-27
@Version: 0.01
"""


class ProjectInfo:
    def __init__(self, artifactId: str, main_class: str, version: str):
        self.artifactId = artifactId
        self.main_class = main_class
        self.version = version
