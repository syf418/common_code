# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/12 16:40
@Author  : shangyf
@File    : 6.键值对RDD.py
'''
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("APP")
sc = SparkContext(conf=conf)

'''
计算每种图书的每天平均销量
'''
rdd1 = sc.parallelize([("Spark", 2), ("Hadoop", 6), ("Hadoop", 4), ("Spark", 6)], 2).cache()
print(rdd1.map(lambda x:(x, 1)).collect())
print(rdd1.mapValues(lambda x:(x, 1)).collect())
rdd2 = rdd1.mapValues(lambda x:(x,1)).reduceByKey(lambda x,y:(x[0]+y[0], x[1]+y[1])).\
        mapValues(lambda x:x[0] / x[1])
print(rdd2.collect())
