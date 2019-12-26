# -*- coding: utf-8 -*-
'''
@Time    : 2019/6/7 13:31
@Author  : shangyf
@File    : spark4_Serializers.py
'''
from pyspark import SparkContext, SparkConf, SparkFiles
from pyspark.serializers import MarshalSerializer
import os
import pandas as pd
from pyspark.sql import SQLContext

os.environ["SPARK_HOME"] = 'E:\spark\spark-2.4.3-bin-hadoop2.7'
os.environ["PYTHONPATH"] = 'E:\spark\spark-2.4.3-bin-hadoop2.7\python'


if __name__ == "__main__":
    sc = SparkContext("local", 'serialization app', serializer=MarshalSerializer())

    print(sc.parallelize(list(range(100))).map(lambda x : 2*x).take(10))
    sc.stop()