#!/usr/bin/env python3
# encoding: utf-8

"""
@File: pom_tools.py
@Author: septemberhx
@Date: 2018-12-25
@Version: 0.01
"""

from typing import *
from xml.dom import minidom


class PomTools:
    """
    Tools to modify pom.xml
    """
    def __init__(self, raw_file_path):
        self.dom = minidom.parse(raw_file_path)  # type: minidom.Document

    def change_main_class(self, new_main_class_name):
        self.change_path_data('project/build/plugins/plugin/executions/execution/configuration/transformers/transformer/mainClass'.split('/'), new_main_class_name)

    def change_artifactId(self, new_artifactId):
        self.change_path_data('project/artifactId'.split('/'), new_artifactId)

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            self.dom.writexml(file)

    def get_main_class(self):
        return self.get_path_data('project/build/plugins/plugin/executions/execution/configuration/transformers/transformer/mainClass'.split('/'))

    def get_path_data(self, tags: List[str]):
        """
        get specific text node according to tags which are the tag path and return it in a list
        :param tags: tag path list which begins with root node tag
        :return: List[str]
        """
        root = self.dom.documentElement  # type: minidom.Document
        current_document_list = []
        next_document_list = [root]
        for i in range(0, len(tags)):
            current_document_list = next_document_list[:]
            next_document_list.clear()
            for current_document in current_document_list:
                if current_document.nodeName == tags[i] and i + 1 != len(tags):
                    for child_node in current_document.childNodes:
                        if child_node.nodeName == tags[i + 1]:
                            next_document_list.append(child_node)
        result_list = []
        for node in current_document_list:
            if node.hasChildNodes():
                result_list.append(node.childNodes[0].data)
        return result_list

    def change_path_data(self, tags: List[str], new_data: str):
        """
        change specific text node to new_data according to tags which are the tag path
        :param tags: tag path list which begins with root node tag
        :param new_data:
        :return:
        """
        root = self.dom.documentElement  # type: minidom.Document
        current_document_list = []
        next_document_list = [root]
        for i in range(0, len(tags)):
            current_document_list = next_document_list[:]
            next_document_list.clear()
            for current_document in current_document_list:
                if current_document.nodeName == tags[i] and i + 1 != len(tags):
                    for child_node in current_document.childNodes:
                        if child_node.nodeName == tags[i + 1]:
                            next_document_list.append(child_node)
        for node in current_document_list:
            if node.hasChildNodes():
                node.childNodes[0].data = new_data


if __name__ == '__main__':
    pom_tools = PomTools("/Users/septemberhx/pom.xml")
    pom_tools.change_artifactId('doom4')
    pom_tools.change_main_class('com.septemberhx.doom4')
    pom_tools.save_to_file('/Users/septemberhx/pom2.xml')
