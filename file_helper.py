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
import re

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

        cmd = "find " + os.path.abspath(origin_path) + " -name '" + base + "*jpg' -maxdepth 1 | xargs -i mv {} " + target_dir
        os.system(cmd)


def make_log(log_msg, stdout=True, log_file=None, log_obj=None, log_mode='a'):
    '''
    Desc：
        记录日志，若stdout为True则输出到屏幕，如果log_file路径非None，则同时记录到文件，若log_obj非None，则使用全局变量log_obj，否则使用log_file新建对象
    Args：
        log_msg: string  --  待记录日志
        stdout: boolean  --  是否输出到屏幕就
    Returns：
        log_file: string  --  输出文件路径，在log_obj为None时生效
    '''
    if stdout:
        print(log_msg)
    if log_file is not None and log_obj is not None:
        log_obj.write(log_msg + '\n')
    elif log_file is not None and log_obj is None:
        with open(log_file, log_mode) as obj:
            obj.write(log_msg + '\n')


def extract_seq_from_text(pattern, text_path, save_path=None):
    '''
    Desc：
        从text_path中按照patten提取内容，并返回
    Args：
        pattern: re.Pattern  --  正则re.compile后的对象
        text_path: string  --  文本路径，若为目录则提取所有文件，若为单个文件则直接提取
        save_path: string  --  结果保存路径，若为None则不保存，直接返回
    Returns：
        res: list  --  提取出的序列
    '''
    text_files = []
    res = []

    # get text files
    if os.path.isdir(text_path):
        for root, subdir, files in os.walk(text_path):
            files = [os.path.join(root, f) for f in files]
            text_files.extend(files)
    elif os.path.isfile(text_path):
        text_files.append(text_path)
    else:
        raise (ValueError("Error: text_path is neither a dir nor a file"))

    # get files content
    for f in text_files:
        with open(f) as fp:
            lines = ' '.join(fp.readlines())
            seq = pattern.findall(lines)
            res.extend(seq)

    # remove redundant seqs
    res = list(set(res))

    # save results
    if save_path is not None:
        with open(save_path, 'w') as fw:
            fw.writelines([x + ',\n' for x in res])

    return res
