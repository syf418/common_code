# -*- coding: utf-8 -*-
'''
@Time    : 2019/6/6 17:29
@Author  : shangyf
@File    : pyspark5_MLlib.py
'''
from pyspark import SparkContext, SparkConf, SparkFiles
from pyspark.mllib import regression
from pyspark.sql import SparkSession
import os
import pandas as pd
from pyspark.sql import SQLContext

os.environ["SPARK_HOME"] = 'E:\spark\spark-2.4.3-bin-hadoop2.7'
os.environ["PYTHONPATH"] = 'E:\spark\spark-2.4.3-bin-hadoop2.7\python'

if __name__ == "__main__":
    '''
    Apache Spark提供了一个名为 MLlib 的机器学习API。PySpark也在Python中使用这个机器学习API。它支持不同类型的算法，如下所述
        mllib.classification - spark.mllib 包支持二进制分类，多类分类和回归分析的各种方法。分类中一些最流行的算法是 随机森林，朴素贝叶斯，决策树 等。
        mllib.clustering - 聚类是一种无监督的学习问题，您可以根据某些相似概念将实体的子集彼此分组。
        mllib.fpm - 频繁模式匹配是挖掘频繁项，项集，子序列或其他子结构，这些通常是分析大规模数据集的第一步。 多年来，这一直是数据挖掘领域的一个活跃的研究课题。
        mllib.linalg - 线性代数的MLlib实用程序。
        mllib.recommendation - 协同过滤通常用于推荐系统。 这些技术旨在填写用户项关联矩阵的缺失条目。
        spark.mllib - 它目前支持基于模型的协同过滤，其中用户和产品由一小组可用于预测缺失条目的潜在因素描述。 spark.mllib使用交替最小二乘（ALS）算法来学习这些潜在因素。
        mllib.regression - 线性回归属于回归算法族。 回归的目标是找到变量之间的关系和依赖关系。使用线性回归模型和模型摘要的界面类似于逻辑回归案例。
    '''
    # sc = SparkContext('local', "MLlib example")
    sc = SparkSession.builder.master("local").appName("Spark MLlib").getOrCreate()
    df = pd.read_csv("rawdata/iris.csv")
    sqlc = SQLContext(sc)
    data = sc.createDataFrame(df)
    print("data:\n")
    data.show(5)
    # 纯spark读取
    data2 =sc.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(
        'rawdata/iris.csv')
    print("data2:\n")
    data2.show(5)

    # data3 = sc.textFile("rawdata/iris.csv")
    # print(data3.take(5))

