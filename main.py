#!/usr/bin/env python3
# encoding: utf-8

"""
@File: main.py
@Author: septemberhx
@Date: 2018-12-27
@Version: 0.01
"""

from tools import pom_tools, java_tools
import shutil
import os, fnmatch

WORK_DIR = '/Users/septemberhx/test/after'
SRC_DIR = '/Users/septemberhx/test/src'
TEMPLATE_DIR = '/Users/septemberhx/test/template'


def process(artifactId: str, main_class: str, version: str, project_name: str):
    # 1. copy src dir to $WORK_DIR
    shutil.copytree(os.path.join(SRC_DIR, project_name), os.path.join(WORK_DIR, project_name))

    # 2. modify pom.xml
    pom_file_path = os.path.join(WORK_DIR, project_name, 'pom.xml')
    pom = pom_tools.PomTools(pom_file_path)
    old_main_class = pom.get_main_class()[0]

    # 3. copy template files
    split_result = old_main_class.split('.')
    old_main_file_name = split_result[-1]
    new_src_path = os.path.join(WORK_DIR, project_name)

    # Walk through
    fileList = []
    for dName, sdName, fList in os.walk(new_src_path):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, old_main_file_name + '.java'):  # Match search string
                fileList.append(os.path.join(dName, fileName))

    old_main_file_path = fileList[0]
    package_name = '.'.join(split_result[:-1])
    java = java_tools.JavaTools(os.path.join(TEMPLATE_DIR, 'MHttpMainController.java'))
    print(os.path.join(os.path.dirname(old_main_file_path), 'MHttpMainController.java'))
    java.add_to_package(package_name, os.path.join(os.path.dirname(old_main_file_path), 'MHttpMainController.java'))

    main_java = java_tools.JavaTools(os.path.join(TEMPLATE_DIR, 'ApplicationMain.java'))
    main_java.add_to_package(package_name, os.path.join(os.path.dirname(old_main_file_path), 'ApplicationMain.java'))

    # save pom.xml
    pom.change_main_class(package_name + '.' + 'ApplicationMain')
    pom.change_artifactId(artifactId)
    pom.save_to_file(pom_file_path)


if __name__ == '__main__':
    process('test', '1111', '123', 'MFramework')
