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
    if type(origin_file) not in [str, list] or type(target_file) not in [str, list]:
        print("Type error: origin_file and target_file should be string or list")
        exit(1)

    origin_file, target_file = [origin_file], [target_file]
    if len(origin_file) != len(target_file):
        print("Value error: origin_file object size should be consistent with target_file")
        exit(1)

    # create sub dir for each origin file
    target_dir = []
    target_name = []
    try:
        for t in target_file:
            t_dir = os.path.dirname(t)
            target_dir.append(t_dir)
            target_name.append(os.path.basename(t))
            if not os.path.exists(t_dir):
                os.system('mkdir -p ' + t_dir)
    except Exception as e:
        print("==> Error: failed to create target directories.")
        exit(1)

    # convert each origin file to target file
    try:
        for i, f in enumerate(origin_file):
            f = os.path.abspath(f)
            origin_name = os.path.basename(f)

            origin_dir = os.getcwd()
            os.chdir(target_dir[i])
            print("==> Change current work directory to: {}".format(target_dir[i]))

            os.system('cp ' + f + ' .')
            print("==> Copy origin file {} to current directory.".format(os.path.basename(f)))

            print("==> Convert origin file {} to target file {}.".format(origin_name, target_name))
            options = ' '.join(options)
            os.system('convert -density 300 -quality 100 {} {} {}'.format(options, origin_name, target_name[i]))

            os.system('rm ' + origin_name)
            print("==> Remove file " + origin_name)

            os.chdir(origin_dir)

        print("==> Convert successfully!")
    except Exception as e:
        print("==> Convert error:\n" + str(e))
