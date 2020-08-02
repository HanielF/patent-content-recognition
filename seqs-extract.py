#!/usr/bin/env python
# coding=utf-8
'''
 * @File    :  test.py
 * @Time    :  2020/06/24 10:58:31
 * @Author  :  Hanielxx
 * @Version :  1.0
 * @Desc    :  None
'''
import os
import re
from file_helper import *

if __name__ == "__main__":
    fr_path = './text'
    fw_path = './siRNA-sequence.csv'

    res = []
    pattern = re.compile(r'[NAUGCT]{15,}', re.I)

    res = extract_seq_from_text(pattern, fr_path)
    res = list(set(res))

    selection = []
    for i in res:
        if len(i) <= 30:
            selection.append(i)

    with open(fw_path, 'w') as fw:
        fw.writelines([x + ',\n' for x in selection])

    print("共查找到 {} 个符合要求的序列".format(len(selection)))
