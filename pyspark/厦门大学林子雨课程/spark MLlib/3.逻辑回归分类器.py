# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/23 23:36
@Author  : shangyf
@File    : 3.逻辑回归分类器.py
'''
from pyspark import SparkConf
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import StringIndexer, IndexToString, \
    VectorIndexer
from pyspark.ml.linalg import Vectors
from pyspark.sql import Row
from pyspark.sql import SparkSession

conf = SparkConf().setMaster("local[4]").setAppName("test3")
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

lr = LogisticRegression().\
        setLabelCol("indexedLabel").\
        setFeaturesCol("indexedFeatures").\
        setMaxIter(100).\
        setParams(regParam=0.3).\
        setElasticNetParam(0.8)

lrPipeline = Pipeline().setStages([labelIndexer, featureIndexer, lr, labelConverter])

trainingData, testData = data.randomSplit([0.7,0.3])
lrPipelineModel = lrPipeline.fit(trainingData)
lrPredictions = lrPipelineModel.transform(testData)

preRel = lrPredictions.select(
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
lrAccuracy = evaluator.evaluate(lrPredictions)
print("准确率：", lrAccuracy)

# 查看模型
lrModel = lrPipelineModel.stages[2]
print("Coefficients:\n" + str(lrModel.coefficientMatrix) + \
        "\n Intercept:" + str(lrModel.interceptVector) + \
        "\n numClasses:" + str(lrModel.numClasses) + \
        "\n numFeatures:" + str(lrModel.numFeatures))