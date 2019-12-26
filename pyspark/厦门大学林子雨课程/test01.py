# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/1 15:49
@Author  : shangyf
@File    : test01.py
'''
'''
pyspark --master <master-url>
'''
# WordCount
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName("my app")
sc = SparkContext(conf=conf)
logFile = "./data/text_1201.txt"
logData = sc.textFile(logFile,2).cache()
numAs = logData.filter(lambda line: 'a' in line).count()
numBs = logData.filter(lambda line: 'b' in line).count()
print("a count:{}, b count:{}".format(numAs, numBs))