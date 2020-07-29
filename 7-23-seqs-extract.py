#!/usr/bin/env python
# coding=utf-8
'''
 * @File    :  test.py
 * @Time    :  2020/06/24 10:58:31
 * @Author  :  Hanielxx
 * @Version :  1.0
 * @Desc    :  None
'''
import os
import re

if __name__ == "__main__":
    # text_files = []
    # for root, subdir, files in os.walk('./text/7-23-image'):
    #     files = [os.path.join(root, f) for f in files]
    #     text_files.extend(files)

    # res = []
    # patten = re.compile(r'[NAUGCT]{19,}', re.I)

    # for f in text_files:
    #     with open(f, 'r') as fp:
    #         lines = fp.readlines()
    #         for line in lines:
    #             seq = patten.findall(line)
    #             res.extend(seq)

    # print("共查找到 {} 个符合要求的序列".format(len(res)))

    # res = [x + ',\n' for x in res]
    # with open('./text/7-23-image/siRNA-seqs.csv', 'w') as fw:
    #     fw.writelines(res)

    f = open('./text/7-23-image-general/siRNA-seqs-general.csv')
    seq_general = f.readlines()
    f.close()

    f = open('./text/7-23-image/siRNA-seqs.csv')
    seq_accu = f.readlines()

    res = list(set(seq_general).union(set(seq_accu)))

    print("accurate识别出{}条序列，去重后还剩{}条".format(len(seq_accu),
                                             len(list(set(seq_accu)))))
    print("general识别出{}条序列，去重后还剩{}条".format(len(seq_general),
                                            len(list(set(seq_general)))))
    print("共识别出{}条序列".format(len(res)))

    with open('./text/7-23-image/siRNA-conbine.csv', 'w') as fp:
        fp.writelines(res)

