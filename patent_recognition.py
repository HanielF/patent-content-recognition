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

SUBFOLDER = ''
IMAGEFOLDER = os.path.abspath('./images/20200712012743948/' + SUBFOLDER)
TEXTFOLDER = os.path.abspath('./text/20200712012743948/' + SUBFOLDER)
DATAPATH = './data/'
TARGET_TYPE = 'jpg'

LOGPATH = './log/patent_recognition.log'
LOG_MODE = 'a'


def cal_time(start_time, end_time):
    '''
    Desc：
        计算时间差，返回小时，分钟和秒
    Args：
        start_time  --  开始时间
        end_time  --  结束时间
    Returns：
        elapsed_hours, elapsed_mins, elapsed_secs  --  经过的小时，分钟，秒
    '''
    if end_time < start_time:
        raise ValueError("结束时间不可小于开始时间")
    elapsed_time = end_time - start_time
    elapsed_hours = int(elapsed_time // 3600)
    elapsed_mins = int((elapsed_time - elapsed_hours * 3600) // 60)
    elapsed_secs = int(elapsed_time - elapsed_mins * 60 - elapsed_hours * 3600)
    return elapsed_hours, elapsed_mins, elapsed_secs


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
        # continue if images i was recognized before
        if os.path.exists(text_path[i]) and os.path.getsize(text_path[i]) > 0:
            continue

        make_log("==>\t\tcurrent image: {}".format(os.path.basename(img)), True, LOGPATH)

        # recognize current pic
        ocr_response = ocr_obj.get_img_text(img)
        img_text = ocr_response.get("words_result")

        # get error code and message
        error_code = ocr_response.get("error_code")
        error_msg = ocr_response.get("error_msg")

        # request again if error occurs
        if error_code is not None:
            error_cnt = 0
            make_log("==> Request error: error_code={}, error_msg={}".format(error_code, error_msg), True, LOGPATH)

            # repeat request several times
            while (error_code == 18 and error_cnt <= 20):
                time.sleep(0.5)
                error_cnt += 1
                make_log("==> QPS error, Request again", True, LOGPATH)

                ocr_response = ocr_obj.get_img_text(img)
                img_text = ocr_response.get("words_result")
                error_code = ocr_response.get("error_code")
                error_msg = ocr_response.get("error_msg")

            # exit in some cases
            if error_code in [4, 14, 17, 19, 100, 110, 111, 216100, 216101, 216102, 216103, 216110, 282003, 282110, 282111]:
                make_log("==> System exit 1", True, LOGPATH)
                sys.exit(1)

        # save results of ocr
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
    st_time_stamp = time.time()
    st_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(st_time_stamp))
    make_log("\n\n" + "=" * 50, True, LOGPATH)
    make_log("==> Start at {}".format(st_time), True, LOGPATH)

    # # get pdf files base name
    # origin_path = get_dir_files(DATAPATH, True)
    # origin_basename = [os.path.basename(x) for x in origin_path]
    # make_log("==> Get files from {}".format(DATAPATH), True, LOGPATH)

    # # get target path to save images
    # target_name = [x.split('.')[0] + '.' + TARGET_TYPE for x in origin_basename]
    # target_path = [os.path.join(IMAGEFOLDER, x.split('.')[0] + '.' + TARGET_TYPE) for x in origin_basename]

    # # convert pdf files and classify other images
    # make_log("==> Start converting pdf files to images", True, LOGPATH)
    # convert.convert(origin_path, target_path)

    make_log("==> Start classifing images in {}".format(IMAGEFOLDER), True, LOGPATH)
    images_classify(IMAGEFOLDER, IMAGEFOLDER, False)

    # combine directories created in converting with that created in classifying
    # target_subdirs = [os.path.abspath(x).split('.')[0] for x in target_path]

    # target_subdirs: abspath of image folders
    target_subdirs = []
    for img_roots, img_subdirs, img_files in os.walk(IMAGEFOLDER):
        img_subdirs = [os.path.join(os.path.abspath(img_roots), x) for x in img_subdirs]
        target_subdirs = list(set(target_subdirs + img_subdirs))

    # create ocr object
    make_log("==> Create baidu ocr object with language_type={} request={}".format(LANGUAGE_TYPE, REQUEST.split('/')[-1]), True, LOGPATH)
    ocr = baidu_ocr.Baidu_OCR(AK,
                              SK,
                              REQUEST,
                              language_type=LANGUAGE_TYPE,
                              detect_direction=DETECT_DIRECTION)

    # recognize images with ocr object and save in TEXTFOLDER
    make_log("==> Start recognizing images and results will be saved in {}".format(TEXTFOLDER), True, LOGPATH)
    # target_subdirs are images directories
    for subdir in target_subdirs:
        # get current text directory
        text_base_dir = os.path.basename(subdir)
        text_subdir = subdir.replace(IMAGEFOLDER, TEXTFOLDER)

        # make log
        cur_time_stamp = time.time()
        h, m, s = cal_time(st_time_stamp, cur_time_stamp)
        make_log("==> Start processing images in \t({}h:{}m:{}s passed)\n\t\t{}".format(h, m, s, subdir), True, LOGPATH)

        # create it if not exist
        if not os.path.exists(text_subdir):
            os.system('mkdir -p ' + text_subdir)

        # skip current image directory
        if len(os.listdir(text_subdir)) == len(os.listdir(subdir)):
            make_log("==> {} has already been processed, skip".format(text_base_dir), True, LOGPATH)
            # continue

        # get all of images
        images_path = get_dir_files(subdir, extend_path=True, recur=False)
        if len(images_path) == 0 or images_path is None:
            make_log("==> There are no pictures in {}, continue".format(text_base_dir), True, LOGPATH)
            continue

        text_basename = [os.path.basename(x).split('.')[0] + '.txt' for x in images_path]
        text_path = [os.path.join(text_subdir, x) for x in text_basename]

        img_text = recognize_img(images_path, ocr, text_path, save=True)

    # record end time
    end_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    make_log("==> End at {}".format(end_time), True, LOGPATH)
    make_log("\n\n" + "=" * 50, True, LOGPATH)