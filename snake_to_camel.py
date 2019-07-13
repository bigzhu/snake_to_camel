#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
from tempfile import mkstemp
from shutil import move
import replace


def findSnake(content):
    '''
    >>> findSnake("_big fuck_zhu gaga_dku kk_z")
    {'a_d': 'aD', 'k_z': 'kZ'}
    '''

    result = re.findall(r'[a-z]_[a-z]', content)
    # 转换数据对的同时实现排重
    trans_pair = dict((k, transToCamel(k)) for k in result)
    return trans_pair


def transToCamel(txt):
    '''
    >>> transToCamel("a_b")
    'aB'
    '''
    return txt[0]+txt[2].upper()


def replaceSnake(file_path):
    '''进行替换
    >>> replace('test.txt')
    '''
    # Create temp file
    old_file = open(file_path)
    print('替换: ' + file_path)
    old_file.seek(0)
    old_file = open(file_path)
    fh, abs_path = mkstemp()
    new_file = open(abs_path, 'w')
    for line in old_file:
        new_line = line
        # 找到需要替换的字符并且循环
        for k, v in findSnake(line).items():
            new_line = new_line.replace(k, v)
        new_file.write(new_line)
    # close temp file
    new_file.close()
    os.close(fh)
    old_file.close()
    # Remove original file
    os.remove(file_path)
    # Move new file
    move(abs_path, file_path)


if __name__ == '__main__':
    #import doctest
    #doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
    path = os.getcwd()
    file_paths = replace.getFilePath(path)
    for file_path in file_paths:
        replaceSnake(file_path)
