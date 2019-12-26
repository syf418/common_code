# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/23 14:56
@Author  : shangyf
@File    : 连接数据库.py
'''
from pyspark import SparkConf
from pyspark.sql import SparkSession, Row

# ！！！ 需要先配置 jbdc
conf = SparkConf().setMaster("local[2]").setAppName("text")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
jbdcDF = spark.read.format('jbdc').\
            option("driver", "com.mysql.jbdc.Driver").\
            option("url", "jbdc:mysql://localhost:3306/spark").\
            option("database", "mysql").\
            option("user", 'root').\
            option("password", '938140').\
            load()
jbdcDF.show()



import sys
sys.exit(0)

import pymysql.cursors

# 连接数据库
connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='938140',
    db='mysql',
    charset='utf8')

# 获取游标
cursor = connect.cursor()
sql = 'SELECT * FROM test_aaa'

result = cursor.execute(sql)
print('result:',result)
# s = cursor.fetchall()
# print("s:", s)
result_list = []
for row in cursor.fetchall():
    print(row)
    result_list.append(row[0])
print("result_list:", result_list)

# 关闭连接
cursor.close()
connect.close()
