# -*- coding: utf-8 -*-
'''
@Time    : 2019/5/4 21:04
@Author  : shangyf
@File    : spark1.py
'''
import warnings

warnings.filterwarnings(action="ignore")

# 一.创建RDD: 并行化一个列表，或者直接读取文件
# 1.1.初始化SparkSession
import pandas as pd
from pyspark.sql import SparkSession, SQLContext
from pyspark import SparkContext
from pyspark.sql.types import *

import os
# os.environ['JAVA_HOME'] = 'D:\Java\jdk'
# os.environ["SPARK_HOME"] = 'D:\Spark\spark-2.2.1-bin-hadoop2.6'
# spark = SparkSession.builder.appName("test").master("local").getOrCreate()
sc = SparkContext('local', 'first app')
'''
Spark1的写法如下：
conf = SparkConf().setMaster('local[10]').setAppName('PySparkShell')
sc = SparkContext.getOrCreate()
sqlContest = SQLContext(sc)
'''
# a.并行化一个集合
data = sc.parallelize([('Amber', 22), ('Alfred', 23), ('Skye', 4), ('Albert', 12), ('Amber', 9)])
'''
PySpark类的详细信息以及SparkContext可以采用的参数:
class pyspark.SparkContext (
   master = None,
   appName = None, 
   sparkHome = None, 
   pyFiles = None, 
   environment = None, 
   batchSize = 0, 
   serializer = PickleSerializer(), 
   conf = None, 
   gateway = None, 
   jsc = None, 
   profiler_cls = <class 'pyspark.profiler.BasicProfiler'>
)
以下是SparkContext的参数具体含义：
    Master- 它是连接到的集群的URL。
    appName- 您的工作名称。
    sparkHome - Spark安装目录。
    pyFiles - 要发送到集群并添加到PYTHONPATH的.zip或.py文件。
    environment - 工作节点环境变量。
    batchSize - 表示为单个Java对象的Python对象的数量。设置1以禁用批处理，设置0以根据对象大小自动选择批处理大小，或设置为-1以使用无限批处理大小。
    serializer- RDD序列化器。
    Conf - L {SparkConf}的一个对象，用于设置所有Spark属性。
    gateway  - 使用现有网关和JVM，否则初始化新JVM。
    JSC - JavaSparkContext实例。
    profiler_cls - 用于进行性能分析的一类自定义Profiler（默认为pyspark.profiler.BasicProfiler）。
    在上述参数中，主要使用master和appname。
'''

# b.读取文件
data_from_file = sc.\
    textFile(
    'rawdata/iris.csv',
    4) # 代表该数据集被划分的分区个数。
# 经验法则是把每一个集群中的数据集分成2到4个分区；

# 二.查看RDD内容
# 2.1.小数据量：通过转换函数collect()转换成一个数组
print("data:", data.collect())
# 2.2.大数据量：take(n)
print("data_from_file:", data_from_file.take(5))
print("data_from_file[1]:", data_from_file.take(1))

# 三.混用数据类型
data_3 = sc.parallelize([
    ("Ferrari", 'fast'),
    {'Porsche': 100000},
    ["Spain", 'visited', 4504]
]).collect()
print('data_3:', data_3[2])
print("data_3:", data_3[1]['Porsche'])