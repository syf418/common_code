# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/9 21:28
@Author  : shangyf
@File    : 常用的键值对RDD转换操作.py
'''
'''
reduceByKey(func):
groupByKey()
'''
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("my app")
sc = SparkContext(conf=conf)

pairRDD = sc.parallelize([("spark",1), ("spark", 2), ("hadoop", 5)])
pairRDD.groupByKey().foreach(print)

words = ["one", "two", "two", "three", "three", "three"]
rdd = sc.parallelize(words).map(lambda x:(x, 1))
rdd_rbk = rdd.reduceByKey(lambda a,b: a+b)
rdd_rbk.foreach(print)

print("------------")
rdd_gbk = rdd.groupByKey()
rdd_gbk.foreach(print)
rdd_gbk1 = rdd_gbk.map(lambda x: (x[0],sum(x[1])))
rdd_gbk1.foreach(print)