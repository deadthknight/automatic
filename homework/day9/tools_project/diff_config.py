#!/usr/bin/env python3
# -*- coding=utf-8 -*-


from difflib import *
import os


def diff_file(file1, file2):
    txt1 = open(file1, 'r').readlines()
    txt2 = open(file2, 'r').readlines()
    result = Differ().compare(txt1, txt2)
    return_result = os.linesep.join(list(result))
    return return_result


def diff_txt(txt1, txt2):
    txt1_list = txt1.split(os.linesep)
    txt2_list = txt2.split(os.linesep)
    result = Differ().compare(txt1_list, txt2_list)
    return_result = os.linesep.join(list(result))
    return return_result


if __name__ == '__main__':
    pass

