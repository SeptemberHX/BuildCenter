#!/usr/bin/env python3
# encoding: utf-8

"""
@File: java_tools.py
@Author: septemberhx
@Date: 2018-12-27
@Version: 0.01
"""


class JavaTools:
    def __init__(self, file_path):
        self.file_path = file_path

    def add_to_package(self, package_name: str, new_file_path: str):
        """
        Insert 'package $package_name' into the begin of the file
        And save the new file to target file path
        :param package_name: target package name
        :return:
        """
        old_content_lines = []
        with open(self.file_path, 'r') as file:
            old_content_lines = file.readlines()
        old_content_lines.insert(0, 'package {0};  // inserted by java_tools.py\n\n'.format(package_name))

        with open(new_file_path, 'w') as file:
            file.writelines(old_content_lines)


if __name__ == '__main__':
    java_tools = JavaTools('/Users/septemberhx/MHttpMainController.java')
    java_tools.add_to_package('com.septemberhx.test', '/Users/septemberhx/1.java')
