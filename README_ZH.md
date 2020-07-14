# patent-content-recognition

[Englist README](README.md)

## 介绍

一个集合1)批量PDF转图片，2)使用 OCR 技术识别PDF文件的内容，3)然后从中提取特定信息等功能的的小项目  
这里主要用于对专利文件内容的识别和信息提取

<!-- TOC -->

- [patent-content-recognition](#patent-content-recognition)
  - [介绍](#介绍)
  - [步骤和思路](#步骤和思路)
  - [文件说明](#文件说明)
  - [开始使用](#开始使用)
    - [创建百度OCR实例](#创建百度ocr实例)
    - [克隆项目](#克隆项目)
    - [创建目录并准备PDF](#创建目录并准备pdf)
    - [修改配置](#修改配置)
    - [运行程序](#运行程序)

<!-- /TOC -->

## 步骤和思路

1. 将 pdf 转换为图片

  + 使用 java 转换
  + 使用 python 转换
  + 使用现有的本地/在线工具手动转换
  + 使用 ImageMagick，编写脚本批量转换
  + 使用 Acrobat
  + ...

2. 对图片使用 OCR

  + 需考虑到内容有的是横版有的是竖版
  + 考虑使用百度/腾讯/阿里的 OCR
  + 百度 OCR，免费额度：通用版 50000 次/天，高精度 500 次/天
  + 使用 Adobe Acrobat 识别
  + 本地设计并训练模型进行 OCR 识别

3. 对识别的文本内容进行处理

  + 通过一些关键词/词频进行一个初筛
  + 识别结果按行排列，处理时注意存在两栏的内容被合并到一行的情况

4. [可选] 对 RNA/DNA 部分进行筛选和提取

  + 提取 RNA/DNA，正则表达式 or 其他字符串匹配方法
  + 本地 blast 判断是否识别正确
  + 去掉修饰的部分

## 文件说明

| 文件名                 | 说明           | 备注                                                                                            |
|-----------------------|----------------|-------------------------------------------------------------------------------------------------|
| baidu_ocr.py          | 包含OCR对象     | 使用[百度OCR](https://ai.baidu.com/tech/ocr/general)                                             |
| convert.py            | PDF转图片       | 使用[Imagemagick Convert](https://github.com/ImageMagick/ImageMagick)                           |
| patent_recognition.py | Main识别文本内容 |                                                                                                 |
| README.md             | 说明文档        |                                                                                                 |
| LICENSE               | 开源协议        | [Apache-2.0 License](https://github.com/HanielF/patent-content-recognition/blob/master/LICENSE) |

| 目录名  | 说明          | 备注                          |
|--------|---------------|-------------------------------|
| data   | 存放待识别PDF  | 将自动识别该目录下所有文件        |
| images | 存放转换后的图片 | 每个文件将自动创建一个子目录      |
| text   | 存放识别的结果  | 对应images目录结构并保存为txt格式 |

## 开始使用

### 创建百度OCR实例

  1. 创建/登录百度帐号
  2. 登录[百度AI开放平台](https://ai.baidu.com/)
  3. 登录控制台
  4. 在文字识别处创建应用
  5. 保存AK，即API Key和SK，即Secret Key

### 克隆项目

``` bash
git clone https://github.com/HanielF/patent-content-recognition.git
```

### 创建目录并准备PDF

```bash
mkdir data images text
```

然后将待识别的PDF文件存放在`data`目录下

### 修改配置

1. 在文件[patent_recognition.py](patent_recognition.py)中修改AK，SK为刚创建应用的API Key和SK

2. 修改`LANGUAGE_TYPE`, `REQUEST`, `DETECT_DIRECTION`等变量控制识别效果

### 运行程序

```bash
python patent_recognition.py
```
