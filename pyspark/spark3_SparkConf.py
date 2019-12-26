# -*- coding: utf-8 -*-
'''
@Time    : 2019/6/6 16:58
@Author  : shangyf
@File    : spark3_SparkConf.py
'''

from pyspark import SparkContext, SparkConf, SparkFiles
import os
import pyspark

os.environ["SPARK_HOME"] = 'E:\spark\spark-2.4.3-bin-hadoop2.7'
os.environ["PYTHONPATH"] = 'E:\spark\spark-2.4.3-bin-hadoop2.7\python'

if __name__ == "__main__":
    # pyspark参数设置：SparkConf()
    '''
    class pyspark.SparkConf (
           loadDefaults = True,
           _jvm = None,
           _jconf = None
        )
    
    以下是SparkConf最常用的一些属性
    set（key，value） - 设置配置属性。
    setMaster（value） - 设置主URL。
    setAppName（value） - 设置应用程序名称。
    get（key，defaultValue = None） - 获取密钥的配置值。
    setSparkHome（value） - 在工作节点上设置Spark安装路径
    '''
    conf = SparkConf().setAppName('Pyspark App').setMaster('local')
    sc = SparkContext(conf=conf)

    # 获取和添加文件路径
    '''
    get(filename): 它指定通过SparkContext.addFile（）添加的文件的路径。
    getrootdirectory（）: 它指定根目录的路径，该目录包含通过SparkContext.addFile（）添加的文件。
    '''
    sc.addFile('rawdata/spark_test.txt')
    path1 = SparkFiles.get('rawdata/spark_test.txt')
    print("path1:", path1)
    path2 = SparkFiles.getRootDirectory()
    print("path2:", path2)

    # RDD存储
    '''
    StorageLevel决定如何存储RDD。在Apache Spark中，StorageLevel决定RDD是应该存储在内存中还是存储在磁盘上，
    或两者都存储。它还决定是否序列化RDD以及是否复制RDD分区。
    
    class pyspark.StorageLevel(useDisk, useMemory, useOffHeap, deserialized, replication = 1)
    
    DISK_ONLY = StorageLevel（True，False，False，False，1）
    DISK_ONLY_2 = StorageLevel（True，False，False，False，2）
    MEMORY_AND_DISK = StorageLevel（True，True，False，False，1）
    MEMORY_AND_DISK_2 = StorageLevel（True，True，False，False，2）
    MEMORY_AND_DISK_SER = StorageLevel（True，True，False，False，1）
    MEMORY_AND_DISK_SER_2 = StorageLevel（True，True，False，False，2）
    MEMORY_ONLY = StorageLevel（False，True，False，False，1）
    MEMORY_ONLY_2 = StorageLevel（False，True，False，False，2）
    MEMORY_ONLY_SER = StorageLevel（False，True，False，False，1）
    MEMORY_ONLY_SER_2 = StorageLevel（False，True，False，False，2）
    OFF_HEAP = StorageLevel（True，True，True，False，1）
    '''
    rdd = sc.parallelize(['a', 'b'])
    print(rdd.collect())
    rdd.persist(pyspark.storagelevel.MEMORY_AND_DISK_2)
    rdd.getStorageLevel()
    print("获取存储类型：",rdd.getStorageLevel())