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

IMAGEFOLDER = './images/'
TEXTFOLDER = './text/'
DATAPATH = './data/'
TARGET_TYPE = 'jpg'

AK = '5aCLlrovDN7DYI6WhIeFGYCN'
SK = 'mkCGTzUxO9xgHkXmht3tGNEfLZNfShmG'
REQUEST = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
LANGUAGE_TYPE = 'auto_detect'
DETECT_DIRECTION = 'true'

def get_dir_files(dir_path=None, extend_path=False):
    '''
    Desc：
        返回dir_path下所有的非目录文件，并以包含路径的形式返回
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
                        tmp_text = text['words'].replace(" ", '')
                        f.write("{}\n".format(tmp_text))
            except Exception as e:
                raise Exception(e)
    return res


if __name__ == "__main__":
    origin_path = get_dir_files(DATAPATH, True)
    origin_basename = [os.path.basename(x) for x in origin_path]

    target_name = [x.split('.')[0] + '.' + TARGET_TYPE for x in origin_basename]
    target_path = [os.path.join(IMAGEFOLDER, x.split('.')[0] + '.' + TARGET_TYPE) for x in origin_basename]

    convert.convert(origin_path, target_path)

    target_subdirs = [os.path.abspath(x).split('.')[0] for x in target_path]

    images_path = get_dir_files(target_subdirs, extend_path=True)
    text_basename = [os.path.basename(x).split('.')[0] + '.txt' for x in images_path]
    text_path = [os.path.join(TEXTFOLDER, x) for x in text_basename]

    ocr = baidu_ocr.Baidu_OCR(AK,
                              SK,
                              REQUEST,
                              language_type=LANGUAGE_TYPE,
                              detect_direction=DETECT_DIRECTION)
    res_text = recognize_img(images_path, ocr, text_path, save=True)
