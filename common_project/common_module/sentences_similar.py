# -*- coding: utf-8 -*-
'''
@Time    : 2019/3/21 17:25
@Author  : shangyf
'''
import time

import distance
import pandas as pd
import jieba
from pypinyin import lazy_pinyin
from operator import itemgetter

# 句子转拼音
def sentence_to_pinyin(text):
    text_pinyin = lazy_pinyin(text)
    text_pinyin = "".join(text_pinyin)
    return text_pinyin

# 计算编辑距离
def edit_distance(s1, s2):
    return distance.levenshtein(s1, s2)

# 句子相似度计算
def sentence_similar(text, sentences):
    '''
    # 分词
    text = list(jieba.cut(text))
    # 去停用词
    with open('rawdata/stopkey.txt', 'r', encoding='utf-8') as f_stop:
        stopkeys = f_stop.read()
    stop_list = stopkeys.split('\n')
    text = [i for i in text if i not in stop_list]
    text = "".join(text)

    text = sentence_to_pinyin(text)
    print("text:", text, flush=True)
    print("sentences[0]:", sentences[0], flush=True)
    '''

    s = None
    index = None
    similar_list = []
    a = 0.6
    for j in range(len(sentences)):
        nums = edit_distance(text, sentences[j])
        if (nums / len(text)) < a:
            s = sentences[j]
            index = j
            a = nums
            similar_list.append((s, nums))
    similar_list = sorted(similar_list, key=itemgetter(1))
    print("similar_list:", similar_list)
    return similar_list, index

if __name__ == "__main__":
    text = "谁在用琵琶弹奏一曲东风破"
    text_pinyin = sentence_to_pinyin(text)
    print("text_pinyin:", text_pinyin)


