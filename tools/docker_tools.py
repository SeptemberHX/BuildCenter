#!/usr/bin/env python3
# encoding: utf-8

"""
@File: docker_tools.py
@Author: septemberhx
@Date: 2019-01-06
@Version: 0.01
"""

from typing import *
from dockerfile_parse import DockerfileParser


class DockerTools:
    def __init__(self, dockerfile_path: str):
        self.dockerfile_path = dockerfile_path
        self.parser = DockerfileParser(dockerfile_path)

    def add_labels(self, labels: Mapping[str, str]):
        for key, value in labels.items():
            self.parser.labels[key] = value

    def modify_entrypoint(self, entrypoint_line: str):
        for inst in self.parser.structure:
            if inst['instruction'] == 'ENTRYPOINT':
                sl = inst['startline']
                el = inst['endline']
                self.parser.lines = self.parser[:sl] + self.parser[el+1:]
        self.parser.add_lines('ENTRYPOINT {0}'.format(entrypoint_line))


