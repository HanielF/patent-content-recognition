#!/usr/bin/env python
# coding=utf-8
'''
 * @File    :  baidu_ocr.py
 * @Time    :  2020/06/19 13:22:39
 * @Author  :  Hanielxx
 * @Version :  1.0
 * @Desc    :  使用百度OCR接口识别图片内容
'''

import requests
import base64
import os.path


class Baidu_OCR:
    def __init__(self,
                 ak,
                 sk,
                 img_path,
                 request_url="https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic",
                 language_type='CHN_ENG',
                 detect_direction='false',
                 paragraph='false',
                 probability='false'):
        '''
        Args：
            ak: string  --  官网获取的API Key
            sk: string  --  官网获取的Secret Key
            img_path: string  --  图像数据，base64编码后进行urlencode，要求base64编码和urlencode后大小不超过4M，
                                  最短边至少15px，最长边最大4096px,支持jpg/jpeg/png/bmp格式
            request_url: string  --  请求的地址，默认通用文字识别高精度类型
                                     通用文字识别："https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
                                     通用文字识别含位置："https://aip.baidubce.com/rest/2.0/ocr/v1/general"
                                     通用文字识别高精度："https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
                                     通用文字识别高精度含位置："https://aip.baidubce.com/rest/2.0/ocr/v1/accurate"
            language_type: string  --  识别语言类型，默认为CHN_ENG，可选值包括：auto_detect：自动检测语言，并识别;
                                       CHN_ENG：中英文混合; ENG：英文; JAP：日语; KOR：韩语; FRE：法语; SPA：西班牙语; POR：葡萄牙语; GER：德语; ITA：意大利语; RUS：俄语; DAN：丹麦语; DUT：荷兰语; MAL：马来语; SWE：瑞典语; IND：印尼语; POL：波兰语; ROM：罗马尼亚语; TUR：土耳其语; GRE：希腊语; HUN：匈牙利语
            detect_direction: string  --  是否检测图像朝向，默认不检测，即：false。
                                          朝向是指输入图像是正常方向、逆时针旋转90/180/270度。可选值包括: true：检测朝向；false：不检测朝向
            paragraph: string  --  是否输出段落信息
            probability: string  --  是否返回识别结果中每一行的置信度
        '''
        self.ak = ak
        self.sk = sk

        if self.img_path is None:
            raise ValueError("Error: Please input img_path!")
        if not os.path.isfile(img_path):
            raise ValueError("Error: img file does not exist!")
        self.img_path = img_path

        self.access_token = self.get_access_token(ak, sk)
        self.request_url = request_url + "?access_token=" + access_token

        self.language_type = language_type
        self.detect_direction = detect_direction
        self.paragraph = paragraph
        self.probability = probability

    def get_access_token():
        '''
        Desc：
            获取access_token并返回
        Returns：
            access_token: string  --  获取到的access_token
        '''
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
            self.ak, self.sk)
        response = requests.get(host)
        return response.json()

    def get_img_text():
        '''
        Desc：
            使用百度OCR识别图片内容
        Returns：
            res: string  --  识别的结果
        '''
        # 二进制方式打开图片文件
        f = open(self.img_path, 'rb')
        img = base64.b64encode(f.read())

        params = {
            "image": img,
            "language_type": self.language_type,
            "detect_direction": self.detect_direction,
            "paragraph": self.paragraph,
            "probability": self.probability
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.request_url, data=params, headers=headers)
        return response.json()
