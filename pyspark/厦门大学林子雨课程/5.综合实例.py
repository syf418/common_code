# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/12 16:34
@Author  : shangyf
@File    : 5.综合实例.py
'''
'''
词频统计
'''
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("APP")
sc = SparkContext(conf=conf)

text = sc.textFile("./data/text_1201.txt")
wordcount = text.flatMap(lambda x: x.split(" ")).map(lambda x:(x, 1)).reduceByKey(lambda a,b: a+b)
print(wordcount.collect())