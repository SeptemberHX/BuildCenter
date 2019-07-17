#!/usr/bin/env python3
# encoding: utf-8

"""
@File: java_tools.py
@Author: septemberhx
@Date: 2018-12-27
@Version: 0.01
"""

chain_list = [
    {
        'class': "com.septemberhx.sampleservice3.controller.OtherController",
        'function': "wrapper"
    },
    {
        'class': 'com.septemberhx.sampleservice1.controller.TestController',
        'function': 'test'
    }
]

dependency_list = [
    {
        'groupId': 'septemberhx',
        'artifactId': 'SampleService3',
        'version': '1.0-SNAPSHOT',
    },
]

pom_dependency_temp = '''
<dependency>
    <groupId>{groupId}</groupId>
    <artifactId>{artifactId}</artifactId>
    <version>{version}</version>
    <scope>compile</scope>
</dependency>
'''


def generate_dependencies(dep_list):
    dep_str = ''
    for dep in dep_list:
        dep_str += pom_dependency_temp.format(**dep)
    return dep_str


def generate_pom_file(dep_list):
    f_c = None
    with open('/home/hexiang/workspace/pycharm/BuildCenter/resource/composition_pom.xml') as template_file:
        f_c = ''.join(template_file.readlines())
        return f_c.format(dependency_list=generate_dependencies(dependency_list))


def generate_object_definition(chain_info):
    body = ''
    index = 0
    for info in chain_info:
        body += '@MFunctionType\n{0} controller{1};\n'.format(info['className'], index)
        index += 1
    return body


def generate_chain_function_body(chain_info):
    body = ""
    index = 0
    for info in chain_info:
        body += 'MResponse r{0} = controller{0}.{1}(body);\n'.format(index, info['functionName'])
        index += 1
    body += 'return r{0};\n'.format(index - 1)
    return body


def generate_com_controller(chain_info):
    f_c = None
    with open('/home/hexiang/workspace/pycharm/BuildCenter/resource/CompositionController.java') as template_file:
        f_c = ''.join(template_file.readlines())
        return f_c.format(definition=generate_object_definition(chain_info), body=generate_chain_function_body(chain_info), path='/test')


def generate_application_yaml(name, register_url):
    f_c = None
    with open('/home/hexiang/workspace/pycharm/BuildCenter/resource/application.yaml') as yaml_file:
        f_c = ''.join(yaml_file.readlines())
        return f_c.format(name=name, register_url=register_url)


if __name__ == '__main__':
    # generate_com_controller(chain_list)
    # print(generate_dependencies(dependency_list))
    # print(generate_pom_file(dependency_list))
    print(generate_application_yaml('MComposition', 8803, 'http://192.168.1.104:5001/eureka'))