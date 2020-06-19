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

IMAGEFOLDER = './images/'
TEXTFOLDER = './text/'

if __name__ == "__main__":
    ak = '5aCLlrovDN7DYI6WhIeFGYCN'
    sk = 'mkCGTzUxO9xgHkXmht3tGNEfLZNfShmG'
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

    img_name = 'test1.png'
    img_path = IMAGEFOLDER + img_name
    text_path = TEXTFOLDER + img_name.split('.')[0] + '.txt'

    ocr = baidu_ocr.Baidu_OCR(ak, sk, request_url, detect_direction='true')
    img_text = ocr.get_img_text(img_path).get("words_result")
    print(img_text)

    with open(text_path, 'w', encoding='utf-8') as f:
        for i in img_text:
            f.write(i['words'] + '\n')

