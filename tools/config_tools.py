#!/usr/bin/env python3
# encoding: utf-8

"""
@File: config_tools.py
@Author: septemberhx
@Date: 2018-12-26
@Version: 0.01
"""

from typing import *
from xml.dom import minidom


class ConfigTools:
    """
    Tools to modify config.xml
    """
    def __init__(self, raw_file_path):
        self.dom = minidom.parse(raw_file_path)  # type: minidom.Document

    def create_service_split_class(self, class_name):
        self.create_path_node('MAdaptor/ServiceSplit/class'.split('/'), class_name)

    def create_service_split_port(self, port):
        self.create_path_node('MAdaptor/ServiceSplit/port'.split('/'), port)

    def create_path_node(self, tags: List[str], data: str):
        """
        add specific text node with data according to tags which are the tag path
        :param tags: tag path list which begins with root node tag
        :param data: target text data
        :return:
        """
        root = self.dom.documentElement  # type: minidom.Document
        current_document_list = []
        next_document_list = [root]
        for i in range(0, len(tags)):
            print(i, tags[i])
            current_document_list = next_document_list[:]
            next_document_list.clear()
            for current_document in current_document_list:
                if current_document.nodeName == tags[i] and i + 1 != len(tags):
                    if_child_node_exists = False
                    for child_node in current_document.childNodes:
                        if child_node.nodeName == tags[i + 1]:
                            if_child_node_exists = True
                            next_document_list.append(child_node)
                    if not if_child_node_exists:
                        node = self.dom.createElement(tags[i + 1])
                        current_document.appendChild(node)
                        next_document_list.append(node)
        for node in current_document_list:
            text_node = self.dom.createTextNode(data)
            node.appendChild(text_node)

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            self.dom.writexml(file)


if __name__ == '__main__':
    config_tools = ConfigTools('/Users/septemberhx/config.xml')
    config_tools.create_service_split_class('com.septemberhx.split')
    config_tools.create_service_split_port('22233')
    config_tools.save_to_file('/Users/septemberhx/config2.xml')
