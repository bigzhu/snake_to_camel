#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
from tempfile import mkstemp
from shutil import move


def findSnake(content):
    '''
    >>> findSnake("_big fuck_zhu gaga_dku kk_z")
    {'a_d': 'aD', 'k_z': 'kZ'}
    '''

    result = re.findall(r'[a-z]_[a-z]', content)
    return {k: transToCamel(k) for k in result}


def transToCamel(txt):
    '''
    >>> transToCamel("a_b")
    'aB'
    '''
    return txt[0]+txt[2].upper()


def replaceSnake(file_path):
    '''进行替换
    >>> replaceSnake('test.txt')
    '''
    # Create temp file
    old_file = open(file_path)
    print(f'替换: {file_path}')
    old_file.seek(0)
    with open(file_path) as old_file:
        fh, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            for line in old_file:
                new_line = line
                for k, v in findSnake(new_line).items():
                    new_line = new_line.replace(k, v)
                new_file.write(new_line)
        os.close(fh)
    # Remove original file
    os.remove(file_path)
    # Move new file
    move(abs_path, file_path)


file_paths = []


def getFilePath(root_path):
    for lists in os.listdir(root_path):
        if lists in ('.git', 'node_modules'):
            continue
        the_path = os.path.join(root_path, lists)
        if os.path.isdir(the_path):
            getFilePath(the_path)
        else:
            file_paths.append(the_path)
    return file_paths


if __name__ == '__main__':
    #import doctest
    #doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
    path = os.getcwd()
    getFilePath(path)
    for file_path in file_paths:
        replaceSnake(file_path)
