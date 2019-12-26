# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/12 14:55
@Author  : shangyf
@File    : 4.持久化_分区.py
'''
from pyspark import SparkConf, SparkContext
# from pyspark.storagelevel import MEMORY_AND_DISK
import pyspark

conf = SparkConf().setMaster("local[2]").setAppName("test4")
sc = SparkContext(conf=conf)

rdd1 = sc.parallelize([1,2,3,5,6], 2).cache() #设置分区数为2, 并持久化
print(rdd1.collect())
rdd1.unpersist() # 移除持久化
rdd2 = rdd1.persist(pyspark.storagelevel.StorageLevel.MEMORY_AND_DISK) #?
# # print(rdd2.collect())
print("分区数：",len(rdd1.glom().collect()))
rdd2 = rdd1.repartition(4) # 重新分区
print("分区数2：",len(rdd2.glom().collect()))

print("自定义分区 --------")
from pyspark import SparkContext, SparkConf

def MyPartitioner(key):
    print("MyPartitioner is running")
    print("The key is %d" % key)
    return key%5

def main():
    print("The main function is running")
    # conf = SparkConf().setMaster("local").setAppName("self partition")
    # sc = SparkContext(conf=conf)
    data = sc.parallelize([1,2,3,4,5,6,1,3,5], 5)
    print(data.collect())
    data2 = data.map(lambda x: (x, 1)).partitionBy(10, MyPartitioner) \
        .map(lambda x: x[0])
    print(data2.collect())

if __name__ == "__main__":
    main()