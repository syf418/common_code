# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/12 10:49
@Author  : shangyf
@File    : 3.RDD行动操作.py
'''
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local[2]").setAppName("TEST3")
sc = SparkContext(conf=conf)

rdd1 = sc.parallelize([1,2,3,4,5,6])
print(rdd1.count())
print(rdd1.first())
print(rdd1.take(3))
print(rdd1.collect())
b = 1
print(rdd1.reduce(lambda a,b: a + b))
print(rdd1.collect())