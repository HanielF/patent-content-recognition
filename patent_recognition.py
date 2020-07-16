#!/usr/bin/env python
# coding=utf-8
'''
 * @File    :  patent_identification.py
 * @Time    :  2020/06/19 14:35:16
 * @Author  :  Hanielxx
 * @Version :  1.0
 * @Desc    :  使用OCR技术完成对专利内容的识别
'''
import baidu_ocr
import convert
import os
import sys
import time
from file_helper import *

AK = '5aCLlrovDN7DYI6WhIeFGYCN'
SK = 'mkCGTzUxO9xgHkXmht3tGNEfLZNfShmG'
REQUEST_GENERAL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
REQUEST_ACCURATE = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
REQUEST = REQUEST_GENERAL
LANGUAGE_TYPE = 'auto_detect'
DETECT_DIRECTION = 'true'

IMAGEFOLDER = './images/' + LANGUAGE_TYPE
TEXTFOLDER = './text/' + LANGUAGE_TYPE
DATAPATH = './data/'
TARGET_TYPE = 'jpg'

LOGPATH = './log/patent_recognition.log'
LOG_MODE = 'a'


def make_log(log_msg, stdout=True, log_file=None, log_obj=None):
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
        with open(log_file, LOG_MODE) as obj:
            obj.write(log_msg + '\n')


def recognize_img(img_path, ocr_obj=None, text_path=None, save=False):
    '''
    Desc：
        识别img_path中的图片，并将结果返回
    Args：
        img_path: string/list(string)  --  图片路径
        ocr_obj: baidu_ocr.BaiDu_OCR  --  ocr对象
        text_path: string/list(string)  --  保存文字路径
        save: bool  --  是否保存结果到text_path
    Returns：
        res: list(list)  --  保存识别的结果
    '''
    # create ocr object
    if ocr_obj is None:
        ocr_obj = baidu_ocr.Baidu_OCR(AK, SK, REQUEST, LANGUAGE_TYPE, DETECT_DIRECTION)

    # handle exception
    img_path = img_path if type(img_path) is list else [img_path]
    if save:
        if text_path is None:
            exit(1)
        text_path = text_path if type(text_path) is list else[text_path]
        if len(text_path) != len(img_path):
            exit(1)

    # recognize img files and save results
    res = []
    for i, img in enumerate(img_path):
        ocr_response = ocr_obj.get_img_text(img)
        img_text = ocr_response.get("words_result")

        error_code = ocr_response.get("error_code")
        error_msg = ocr_response.get("error_msg")

        if error_code is not None:
            error_cnt = 0
            make_log("==> Request error: error_code={}, error_msg={}".format(error_code, error_msg), True, LOGPATH)

            while (error_code == 18 and error_cnt <= 20):
                error_cnt += 1
                make_log("==> QPS error, Request again", True, LOGPATH)

                ocr_response = ocr_obj.get_img_text(img)
                img_text = ocr_response.get("words_result")
                error_code = ocr_response.get("error_code")
                error_msg = ocr_response.get("error_msg")

            if error_code in [4, 14, 17, 19, 100, 110, 111, 216100, 216101, 216102, 216103, 216110, 216201, 282003, 282110, 282111]:
                make_log("==> System exit 1", True, LOGPATH)
                sys.exit(1)

        res.append(img_text)
        if save:
            try:
                with open(text_path[i], 'w', encoding='utf-8') as f:
                    if img_text is not None:
                        for text in img_text:
                            tmp_text = text['words']
                            f.write("{}\n".format(tmp_text))
            except Exception as e:
                raise Exception(e)
    return res


if __name__ == "__main__":
    # record start time
    st_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    make_log("==> Start at {}".format(st_time), True, LOGPATH)
    # get pdf files base name
    origin_path = get_dir_files(DATAPATH, True)
    origin_basename = [os.path.basename(x) for x in origin_path]
    make_log("==> Get files from {}".format(DATAPATH), True, LOGPATH)

    # get target path to save images
    target_name = [x.split('.')[0] + '.' + TARGET_TYPE for x in origin_basename]
    target_path = [os.path.join(IMAGEFOLDER, x.split('.')[0] + '.' + TARGET_TYPE) for x in origin_basename]

    # convert pdf files and classify other images
    make_log("==> Start converting pdf files to images", True, LOGPATH)
    convert.convert(origin_path, target_path)

    make_log("==> Start classifing images in {}".format(IMAGEFOLDER), True, LOGPATH)
    images_classify(IMAGEFOLDER, IMAGEFOLDER, False)

    # combine directories created in converting with that created in classifying
    target_subdirs = [os.path.abspath(x).split('.')[0] for x in target_path]

    # target_subdirs = []
    for img_roots, img_subdirs, img_files in os.walk(IMAGEFOLDER):
        img_subdirs = [os.path.join(os.path.abspath(img_roots), x) for x in img_subdirs]
        target_subdirs = list(set(target_subdirs + img_subdirs))
        break

    # create ocr object
    make_log("==> Create baidu ocr object with language_type={} request={}".format(LANGUAGE_TYPE, REQUEST.split('/')[-1]), True, LOGPATH)
    ocr = baidu_ocr.Baidu_OCR(AK,
                              SK,
                              REQUEST,
                              language_type=LANGUAGE_TYPE,
                              detect_direction=DETECT_DIRECTION)

    # recognize images with ocr object and save in TEXTFOLDER
    make_log("==> Start recognizing images and results will be saved in {}".format(TEXTFOLDER), True, LOGPATH)
    for subdir in target_subdirs:
        text_base_dir = os.path.basename(subdir)
        text_subdir = os.path.join(TEXTFOLDER, text_base_dir)
        make_log("==> Start processing images in \n\t\t{}".format(subdir), True, LOGPATH)

        if not os.path.exists(text_subdir):
            os.system('mkdir -p ' + text_subdir)

        if len(os.listdir(text_subdir)) == len(os.listdir(subdir)):
            make_log("==> {} has already been processed, skip".format(text_base_dir), True, LOGPATH)
            continue

        images_path = get_dir_files(subdir, extend_path=True)
        if len(images_path) == 0 or images_path is None:
            make_log("==> There are no pictures in {}, continue".format(text_base_dir), True, LOGPATH)
            continue

        text_basename = [os.path.basename(x).split('.')[0] + '.txt' for x in images_path]
        text_path = [os.path.join(text_subdir, x) for x in text_basename]

        img_text = recognize_img(images_path, ocr, text_path, save=True)

    # record end time
    end_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    make_log("==> End at {}".format(end_time), True, LOGPATH)
