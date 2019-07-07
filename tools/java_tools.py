#!/usr/bin/env python3
# encoding: utf-8

"""
@File: java_tools.py
@Author: septemberhx
@Date: 2018-12-27
@Version: 0.01
"""


from javalang import parse


if __name__ == '__main__':
    with open('../a.java') as f:
        f_str = '\n'.join(f.readlines())
        j = parse.parse(f_str)
        for t in j.types:
            if 'MCalcUtils' == t.name:
                for m in t.methods:
                    if 'wrapper' == m.name:
                        print(m._position.line)