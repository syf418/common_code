# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/23 22:09
@Author  : shangyf
@File    : 1.机器学习流水线-逻辑回归.py
'''
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local[4]").setAppName("test")
spark = SparkSession.builder.config(conf=conf).getOrCreate()

# 构建数据
training = spark.createDataFrame([
    (0, "a b c d e spark", 1.0),
    (1, 'b, d', 0.0),
    (2, 'spark f g h', 1.0),
    (3, "hadoop mapreduce", 0.0)
    ], ["id", "text", "label"])
training.show()

# 构建流水线
tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
lr = LogisticRegression(maxIter=10, regParam=0.001)
pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])

# 训练
model = pipeline.fit(training)

# 构建测试数据
test = spark.createDataFrame([
    (4, "spark i j k"),
    (5, "l m n")
    ], ["id", "text"])

prediction = model.transform(test)
selected = prediction.select("id", "text", "probability", "prediction")
for row in selected.collect():
    id, text, proba, prediction = row
    print(id, text, proba, prediction)
