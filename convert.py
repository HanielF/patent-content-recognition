#!/usr/bin/env python
# coding=utf-8
'''
 * @File    :  convert.py
 * @Time    :  2020/06/24 10:28:41
 * @Author  :  Hanielxx
 * @Version :  1.0
 * @Desc    :  Convert patent file from PDF to JPG
'''

import os

def convert(origin_file, target_file, options=[]):
    '''
    Desc：
        将origin_file中的文件从origin_type转换为target_type并保存为target_file
    Args：
        origin_file: string/list   --  源文件，包含文件路径
        target_file: string/list   --  目标文件，包含文件路径
        target_type: string        --  目标文件类型
        options:     list(string)  --  可选的convert命令参数
    Returns：
        None
    '''
    if type(origin_file) not in [string, list] or type(target_file) not in [string, list]:
        raise TypeError("Type error: origin_file and target_file should be string or list")

    origin_file, target_file = list(origin_file), list(target_file)
    if len(origin_file) != len(target_file):
        raise ValueError("Value error: origin_file object size should be consistent with target_file")

    # create sub dir for each origin file
    target_dir = []
    target_name = []
    for t in target_file:
        target_dir.append(os.path.dirname(t))
        target_name.append(os.path.basename(t))
        if not os.path.exists(t_dir):
            os.system('mkdir -p ' + t_dir)

    # convert each origin file to target file
    for i, f in enumerate(origin_file):
        f = os.path.abspath(f)
        origin_name = os.path.basename(f)
        os.system('cd ' + target_dir[i])
        os.system('cp ' + f + ' .')
        os.system('convert -density 300 -quality 100 {} {}'.format(origin_name, target_name))
        os.system('cd -')



