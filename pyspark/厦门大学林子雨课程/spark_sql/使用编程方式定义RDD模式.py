# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/23 14:27
@Author  : shangyf
@File    : 使用编程方式定义RDD模式.py
'''
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import Row

from pyspark.sql.types import *

# 生成表头
scString = "start middle end"
fileds = [StructField(field_name, StringType(), True)
          for field_name in scString.split(" ")]
schema = StructType(fileds)

conf = SparkConf().setMaster("local[2]").setAppName("text2")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
lines = spark.sparkContext.\
        textFile("../data/text_1201.txt").\
        map(lambda x: x.split(" ")).\
        map(lambda x: Row(x[0], x[1], x[2]))
# 表头和数据拼接
schedmaText = spark.createDataFrame(lines, schema)
schedmaText.show()
# 注册临时表
schedmaText.createOrReplaceTempView("text")
df = spark.sql("select * from text")
df.show()