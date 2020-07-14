#!/usr/bin/env python
# coding=utf-8
'''
 * @File    :  file_helper.py
 * @Time    :  2020/07/14 16:35:39
 * @Author  :  Hanielxx
 * @Version :  1.0
 * @Desc    :  用于文件处理
'''
import os


def get_files_prefix(path, chr_num=2):
    '''
    Desc：
        获取path下所有文件的前缀集合
    Args：
        path: str  --  文件路径
        chr_num: int  --  前缀字符个数
    Returns：
        prefix: list  --  前缀集合
    '''
    if not os.path.exists(path):
        return []

    prefix = []
    for root, subdirs, files in os.walk(path):
        code = [x[:chr_num] for x in files]
        prefix = list(set(code))

    return prefix


def get_dir_files(dir_path=None, extend_path=False):
    '''
    Desc：
        返回dir_path下所有的非目录文件，并以包含路径的形式返回，也包括子目录下的文件
    Args：
        dir_path: string/list  --  需要遍历的所有目录
        extend_path: Bool  --  是否拼接路径
    Returns：
        res: list(string)  --  以带路径的形式返回所有目录下的文件
    '''
    if dir_path is None:
        return []
    dir_path = dir_path if type(dir_path) is list else [dir_path]

    res = []
    for dir in dir_path:
        for root, sub_dir, file in os.walk(dir):
            if extend_path:
                file = [os.path.join(root, x) for x in file]
            res.extend(file)
    return res

def images_classify(origin_path, target_path, recursive=False):
    '''
    Desc：
        将目录中的图片按照名称分类，并保存在各个子目录中
    Args：
        origin_path: str  --  源文件路径
        target_path: str  --  目标文件目录
        recursize: boolean  --  是否对源文件路径进行递归搜索
    Returns：
        None
    '''
    # exception
    if not os.path.exists(origin_path) or not os.path.exists(target_path):
        sys.exit(0)

    # get images
    images = []
    for root, sub_dir, files in os.walk(origin_path):
        img_file = [x for x in files if x.split('.')[-1] in ['jpg', 'jpeg', 'png']]
        images.extend(img_file)
        if not recursive:
            break

    # get images basename set
    img_base_lst = list(set([x.split('_')[0] for x in images]))

    # create sub dirs and classify images
    for base in img_base_lst:
        target_dir = os.path.join(target_path, base)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        os.system("mv " + os.path.join(origin_path, base) + "* " + target_dir)
