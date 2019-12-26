# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/1 16:56
@Author  : shangyf
@File    : 2.RDD转换操作.py
'''
'''
1.转换类型操作（transformation）：惰性机制，只记录转换的轨迹
    对于RDD而言，每一次转换操作都会产生不同的RDD
    常见的转换操作：
        -1.filter(func):筛选出满足func的元素
        -2.map(func)：将每个元素传递到函数func中
        -3.flatMap(func):
        -4.groupByKey():
        -5.reduceByKey(func):
2.动作类型操作（action）：
'''
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("my app")
sc = SparkContext(conf=conf)

lines =sc.textFile("./data/text_1201.txt").cache()

print('filter -------:')
linesFilter = lines.filter(lambda line: "Spark" in line)
linesFilter.foreach(print)

print("map --------")
linesMap = lines.map(lambda x: x.split(' '))
linesMap.foreach(print)

print("flatMap -------")
linesflatMap = lines.flatMap(lambda x:x.split(" "))
linesflatMap.foreach(print)

print("groupByKey --------")
words = sc.parallelize([("Hadoop", 1), ("is", 1), ("good", 1), ("Spark", 1), ("is", 1), ("fast", 1),
                        ("Spark", 1), ("is", 1), ("better", 1)])
words1 = words.groupByKey()
words1.foreach(print)
# print(":", words1.collect())

print("reduceByKey --------")
words2 = words.reduceByKey(lambda a,b: a+b)
words2.foreach(print)