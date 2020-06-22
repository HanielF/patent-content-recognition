# patent-content-recognition

使用OCR技术识别专利内容，并从中提取特定siRNA序列信息

## 思路
1. 将pdf转换为图片
  - 使用java转换
  - 使用python转换
  - 使用现成的工具手动转换
  - 使用ImageMagick，编写脚本批量转换
2. 对图片使用OCR
  - 有的是横版有的是竖版
  - 使用百度OCR的API，每天免费的次数也够用了
  - 使用Adobe Acrobat识别
  - 自己训练模型OCR识别
3. 对识别的文本内容进行处理
  - 通过一些关键词/词频进行一个初筛
  - 本地blast判断是否识别正确
  - 去掉修饰的部分
  - 数据不大的情况下直接使用mRNA的序列遍历，然后暴力匹配
