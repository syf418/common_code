# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/23 13:53
@Author  : shangyf
@File    : 利用反射机制推断RDD模式.py
'''
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import Row

conf = SparkConf().setMaster("local[8]").setAppName("test 01")
sc = SparkContext(conf=conf)

spark = SparkSession.builder.config(conf=conf).getOrCreate()
text = spark.sparkContext.textFile("../data/text_1201.txt").\
    map(lambda x: x.split(" ")).\
    map(lambda x: Row(start=x[0],middle=x[1],end=x[2]))
schemaText = spark.createDataFrame(text)
schemaText.show()
# 必须注册为临时表才能供下面的查询使用
schemaText.createOrReplaceTempView("text")
schemaText.show()
df1 = spark.sql("select start,end from text where start = 'Spark'")
df1.show()

# RDD
rdd1 = df1.rdd.map(lambda x: "start:" + x.start + ',' + "end:" + x.end)
rdd1.foreach(print)
print(rdd1.collect())