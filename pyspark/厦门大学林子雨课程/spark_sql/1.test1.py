# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/23 13:07
@Author  : shangyf
@File    : 1.test1.py
'''
'''
Spark SQL: 
Hive on Spark:

SparkSession:
'''
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()

df = spark.read.text("../data/text_1201.txt")
df.show()

df.write.text("../data/text_1223.txt")
df.write.parquet("../data/text_1223.parquet")
df.write.format("text").save("../data/text_1223_1.txt")