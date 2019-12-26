# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/1 16:41
@Author  : shangyf
@File    : 1.RDD创建.py
'''
'''
1.textFile():
    支持的数据类型：
        -1.本地文件系统
            "file:/// + path"
        -2.分布式文件系统HDFS："hdfs://localhost:9000/"
        -3.Amazon S3等等（云端）
2.通过并行集合（数组）创建RDD：
    rdd = sc.parallelize(array)
    rdd.foreach(print)
   
'''
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster('local').setAppName("my app")
sc = SparkContext(conf=conf)
# 本地加载
path = "data/text_1201.txt"
lines = sc.textFile(path)
lines.foreach(print)

# parallelize
rdd = sc.parallelize([1,2,3,4,5])
rdd.foreach(print)