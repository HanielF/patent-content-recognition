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

IMAGEFOLDER = './images/'
TEXTFOLDER = './text/'
DATAPATH = './data/'
TARGET_TYPE = 'jpg'

AK = '5aCLlrovDN7DYI6WhIeFGYCN'
SK = 'mkCGTzUxO9xgHkXmht3tGNEfLZNfShmG'
REQUEST_GENERAL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
REQUEST_ACCURATE = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
REQUEST = REQUEST_GENERAL
LANGUAGE_TYPE = 'ENG'
DETECT_DIRECTION = 'true'


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
        img_text = ocr_obj.get_img_text(img).get("words_result")
        res.append(img_text)

        if save:
            try:
                with open(text_path[i], 'w', encoding='utf-8') as f:
                    for text in img_text:
                        tmp_text = text['words']
                        f.write("{}\n".format(tmp_text))
            except Exception as e:
                raise Exception(e)
    return res


if __name__ == "__main__":
    # get pdf files base name
    origin_path = get_dir_files(DATAPATH, True)
    origin_basename = [os.path.basename(x) for x in origin_path]

    # get target path to save images
    target_name = [x.split('.')[0] + '.' + TARGET_TYPE for x in origin_basename]
    target_path = [os.path.join(IMAGEFOLDER, x.split('.')[0] + '.' + TARGET_TYPE) for x in origin_basename]

    # convert pdf files and classify other images
    convert.convert(origin_path, target_path)
    images_classify('./images', './images', False)

    # combine directories created in converting with that created in classifying
    target_subdirs = [os.path.abspath(x).split('.')[0] for x in target_path]
    for img_roots, img_subdirs, img_files in os.walk(IMAGEFOLDER):
        img_subdirs = [os.path.join(os.path.abspath(img_roots), x) for x in img_subdirs]
        target_subdirs = list(set(target_subdirs + img_subdirs))
        break

    # create ocr object
    ocr = baidu_ocr.Baidu_OCR(AK,
                              SK,
                              REQUEST,
                              language_type=LANGUAGE_TYPE,
                              detect_direction=DETECT_DIRECTION)

    # recognize images with ocr object and save in TEXTFOLDER
    res_text = []
    for subdir in target_subdirs:
        text_base_dir = os.path.basename(subdir)
        text_subdir = os.path.join(TEXTFOLDER, text_base_dir)

        if not os.path.exists(text_subdir):
            os.mkdir(text_subdir)

        images_path = get_dir_files(subdir, extend_path=True)
        if len(images_path) == 0 or images_path is None:
            continue
        text_basename = [os.path.basename(x).split('.')[0] + '.txt' for x in images_path]
        text_path = [os.path.join(text_subdir, x) for x in text_basename]

        img_text = recognize_img(images_path, ocr, text_path, save=True)
        res_text.append(img_text)
