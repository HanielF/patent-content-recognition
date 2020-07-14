# patent-content-recognition

## Introduction

It is a simple, practical tool that includes functions of batch converting pdfs to images, recognizing texts in images, and extract information in texts.

Here it was mainly used to recognize texts in patent files and extract RNA/DNA sequences that i need.

<!-- TOC -->

- [patent-content-recognition](#patent-content-recognition)
  - [Introduction](#introduction)
  - [Steps and Ideas](#steps-and-ideas)
  - [File Descriptions](#file-descriptions)
  - [Begin to use](#begin-to-use)
    - [Create Baidu OCR instance](#create-baidu-ocr-instance)
    - [Clone project](#clone-project)
    - [Create directories](#create-directories)
    - [Change configuration](#change-configuration)
    - [Run python files](#run-python-files)

<!-- /TOC -->

## Steps and Ideas

1. Convert PDF to Jpg

- convert with Java
- convert with Python
- convert with existing tools manually
- convert with ImageMagick and shell scripts
- convert with Acrobat
- ...

2. Apply OCR to images

- Images content layout should be considered in advance
- Existing OCR technology providers includes baidu, tencent and alibaba
- It is free to use Baidu OCR within a limited number of times, 50000 times/day for general version and 500 times/day for accurate version
- Recognizing with Adobe Acrobat
- Design and train your OCR model to recognize

3. Process texts recognized before

- Filter with some key words and word frequency
- The texts was saved in lines
- Pay attention to texts that was saved in one line from two columns

4. [Optional] Screen and extract RNA/DNA from texts

- Extract RNA/DNA with regular expression or any other string match functions
- Blast in local to make judgement
- Remove the decorated part in RNA/DNA

## File Descriptions

| File Name             | Descriptions             | Comment                                                                                         |
| --------------------- | ------------------------ | ----------------------------------------------------------------------------------------------- |
| baidu_ocr.py          | include OCR class object | with [百度 OCR](https://ai.baidu.com/tech/ocr/general)                                          |
| convert.py            | convert pdf to images    | with [Imagemagick Convert](https://github.com/ImageMagick/ImageMagick)                          |
| patent_recognition.py | Main file                |                                                                                                 |
| README.md             | Descriptions             |                                                                                                 |
| LICENSE               | Open source license      | [Apache-2.0 License](https://github.com/HanielF/patent-content-recognition/blob/master/LICENSE) |

| Directory Name | Descriptions                       | Comment                                                                         |
| -------------- | ---------------------------------- | ------------------------------------------------------------------------------- |
| data           | contain pdf files to be recognized | files will be detected automatically                                            |
| images         | contain images converted           | sub directories would be created for each origin file                           |
| text           | contain results from ocr           | directory structure is same as images folder and results are saved in txt files |

## Begin to use

### Create Baidu OCR instance

1. Sign up/in [baidu ai studio](https://ai.baidu.com/)
2. Login in console
3. Create ocr instance
4. Save your API Key and Secret Key as AK and SK

### Clone project

```bash
git clone https://github.com/HanielF/patent-content-recognition.git
```

### Create directories

```bash
mkdir data images text
```

Then move your pdf files to be recognized in data folder.

### Change configuration

1. Modify AK and SK parameters in [patent_recognition.py](patent_recognition.py) to your own API Key and Secret Key

2. Change `LANGUAGE_TYPE` , `REQUEST` , `DETECT_DIRECTION` etc. parameters to specify ocr model

### Run python files

```bash
python patent_recognition.py
```
