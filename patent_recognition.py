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

if __name__ == "__main__":
    ak = '5aCLlrovDN7DYI6WhIeFGYCN'
    sk = 'mkCGTzUxO9xgHkXmht3tGNEfLZNfShmG'
    img_path = './images/test1.png'
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

    ocr = baidu_ocr.Baidu_OCR(ak, sk, request_url, detect_direction='true')
    img_text = ocr.get_img_text(img_path)
    print(img_text)
