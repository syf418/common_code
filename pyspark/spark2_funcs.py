# -*- coding: utf-8 -*-
'''
@Time    : 2019/6/6 8:55
@Author  : shangyf
@File    : spark2_funcs.py
'''
'''
pysaprk常用函数以及广播和累积器
'''
from pyspark import SparkContext
from operator import add
import os

os.environ["SPARK_HOME"] = 'E:\spark\spark-2.4.3-bin-hadoop2.7'
os.environ["PYTHONPATH"] = 'E:\spark\spark-2.4.3-bin-hadoop2.7\python'

if __name__ == "__main__":
    sc = SparkContext("local", "firstApp")
    # 计算README.txt文件中带有字符“a”或“b”的行数
    logFile = "rawdata/spark_test.txt"
    logData = sc.textFile(logFile).cache()
    numAs = logData.filter(lambda s: 'a' in s).count()
    numBs = logData.filter(lambda s: 'b' in s).count()
    print("Line with a:%i,lines with b :%i" % (numAs, numBs))

    '''
    RDD: RDD是不可变元素，这意味着一旦创建了RDD，就无法对其进行更改.
    转换(transform) - 这些操作应用于RDD以创建新的RDD。 Filter，groupBy和map是转换的例子。
    操作(action) - 这些是应用于RDD的操作，它指示Spark执行计算并将结果发送回驱动程序。

    class pyspark.RDD (
        jrdd,
        ctx,
        jrdd_deserializer = AutoBatchedSerializer(PickleSerializer())
        )
    '''
    # pyspark基本操作
    print("pyspark基本操作：------------")
    words = sc.parallelize(
        ["scala", "java", "hadoop", "spark", "akka", "spark vs hadoop", "pyspark", "pyspark and spark"]
    )
    counts = words.count()
    print("计数-count():", counts)
    coll = words.collect()
    print("收集-collect():", coll)
    def func_print(x):
        print(x)
    fore = words.foreach(func_print)
    print("foreach函数：", fore)
    words_filter = words.filter(lambda x: "spark" in x)
    filtered = words_filter.collect()
    print("过滤-filter():", filtered)
    words_map = words.map(lambda x: (x, 1))
    mapping = words_map.collect()
    print("mapping:", mapping)

    nums = sc.parallelize([1,2,3,4,5])
    nums_reduce = nums.reduce(add)
    print("reduce:", nums_reduce)

    x = sc.parallelize([("spark", 1), ("hadoop", 4)])
    y = sc.parallelize([("spark", 2), ("hadoop", 5)])
    joined = x.join(y)
    final = joined.collect()
    print("join:", final)

    # cache(): 使用默认存储级别（MEMORY_ONLY）保留此RDD。您还可以检查RDD是否被缓存
    words.cache()
    caching = words.persist().is_cached
    print("RDD是否被缓存：", caching)

    # spark广播与累积器
    '''
    Apache Spark支持两种类型的共享变量:
        Broadcast:广播,用于跨所有节点保存数据副本。此变量缓存在所有计算机上，而不是在具有任务的计算机上发送。
        Accumulator：累积器，用于通过关联和交换操作聚合信息，例如使用累加器进行求和操作或计数器。
        
    class pyspark.Broadcast (
           sc = None,
           value = None,
           pickle_registry = None,
           path = None
        )
        
    class pyspark.Accumulator(aid, value, accum_param)
    '''
    print("spark广播与累积器：------------------")
    words_new = sc.broadcast(["scala", "java", "hadoop", "spark", "akka"])
    data = words_new.value
    print("data:", data)
    elem = words_new.value[2]
    print("elem:", elem)

    num = sc.accumulator(10)
    print("num:", num)
    def f(x):
        global num
        num += x
    rdd = sc.parallelize([20,30,40,50])
    rdd.foreach(f)
    final = num.value
    print("final:", final)







