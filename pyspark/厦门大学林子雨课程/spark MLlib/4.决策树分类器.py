# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/24 0:16
@Author  : shangyf
@File    : 4.决策树分类器.py
'''
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors,Vector
from pyspark.ml.classification import DecisionTreeClassificationModel, \
        DecisionTreeClassifier
from pyspark.sql import Row, functions
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, IndexToString,\
    VectorIndexer,HashingTF,IDF,Tokenizer
from pyspark.ml.classification import LogisticRegression,\
    LogisticRegressionModel,\
    BinaryLogisticRegressionSummary
from pyspark.sql import Row

conf = SparkConf().setMaster("local[4]").setAppName("test4")
spark = SparkSession.builder.config(conf=conf).getOrCreate()

def f(x):
    rel = {}
    rel["features"] = Vectors.dense(float(x[0]), float(x[1]), float(x[2]), float(x[3]))
    rel["label"] = str(x[4])
    return rel

data = spark.sparkContext.textFile("../data/iris.txt").\
        map(lambda x: x.split(",")).\
        map(lambda x: Row(**f(x))).\
        toDF()
data.show()

labelIndexer = StringIndexer().setInputCol("label").\
                setOutputCol("indexedLabel").\
                fit(data)

featureIndexer = VectorIndexer().setInputCol("features").\
                setOutputCol("indexedFeatures").\
                setMaxCategories(4).\
                fit(data)

labelConverter = IndexToString().\
            setInputCol("prediction").\
            setOutputCol("predictedLabel").\
            setLabels(labelIndexer.labels)

dc = DecisionTreeClassifier().\
        setLabelCol("indexedLabel").\
        setFeaturesCol("indexedFeatures")

dcPipeline = Pipeline().setStages([labelIndexer, featureIndexer, dc, labelConverter])

trainingData, testData = data.randomSplit([0.7,0.3])
dcPipelineModel = dcPipeline.fit(trainingData)
dcPredictions = dcPipelineModel.transform(testData)

preRel = dcPredictions.select(
    "predictedLabel",
    "label",
    "features",
    "probability").collect()
for item in preRel:
    print(str(item["label"]) + "," +
          str(item["features"]) + "," +
          str(item["probability"]) + "," +
          str(item["predictedLabel"]))

# 评估
evaluator = MulticlassClassificationEvaluator().\
        setLabelCol("indexedLabel").\
        setPredictionCol("prediction")
dcAccuracy = evaluator.evaluate(dcPredictions)
print("准确率：", dcAccuracy)

# 查看模型
dcModel = dcPipelineModel.stages[2]
print("Learned classification tree model:\n" + \
      str(dcModel.toDebugString))
