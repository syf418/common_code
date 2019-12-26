# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/23 22:29
@Author  : shangyf
@File    : 2.特征处理.py
'''
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF

conf = SparkConf().setMaster("local[4]").setAppName("test2")
spark = SparkSession.builder.config(conf=conf).getOrCreate()

# 构建数据
sentenceData = spark.createDataFrame([
    (0, "I heard about Spark and I love Spark"),
    (0, 'I wish Java could use case classes'),
    (1, 'Logistic regression models are neat')]).toDF("label", "sentence")

sentenceData.show()

# 分词
tokenizer = Tokenizer(inputCol="sentence", outputCol="words")
wordsData = tokenizer.transform(sentenceData)
wordsData.show()

# 特征向量表示-TF
hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=2000) # 设置哈希的桶数为2000
featurizedData = hashingTF.transform(wordsData)
featurizedData.select("words", "rawFeatures").show(truncate=False)

idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)
rescaledData = idfModel.transform(featurizedData)
rescaledData.select("features", "label").show(truncate=False)

# StringIndexer: str -> num
'''
StringIndexer转换器可以把一列类别型的特征（或标签）进行编码，使其数值化，索引的范围从
0开始，该过程可以使得相应的特征索引化，使得某些无法接受类别型特征的算法可以使用，并提高
诸如决策树等机器学习算法的效率。
索引构建的顺序为标签的频率，优先编码频率较大的标签，所以出现频率最高的标签为0号。
如果输入数值型的，会先把它转化成字符型，再对其进行编码。
'''
from pyspark.ml.feature import StringIndexer
df = spark.createDataFrame([(0, "a"), (1, "b"), (2, "c"), (3, "b")], ["id", "category"])

indexer = StringIndexer(inputCol="category", outputCol="categoryIndex")
model = indexer.fit(df)
indexed = model.transform(df)
indexed.show()

# IndexToString: num -> str
'''
与StringIndexer相对应，IndexToString的作用是把标签索引的一列重新映射回原有的字符型标签。
其主要使用场景一般都是和StringIndexer配合，先用StringIndexer将标签转换为标签索引，进行
模型训练，然后在预测标签的时候再把标签索引转化成原有的字符标签。
'''
from pyspark.ml.feature import IndexToString

toString = IndexToString(inputCol="categoryIndex", outputCol="originalCategory")
indexString = toString.transform(indexed)
indexString.select("id", "originalCategory").show()

# VectorIndexer:
'''
解决向量数据集中的类别型特征转换。
通过为其提供maxCategories超参数，它可以自动识别哪些特征是类别型的，并且将原始值转换为类
别索引。它基于不同特征值的数量来识别哪些特征需要被类别化，那些取值可能性最多不超过maxCategories
的特征需要会被认为是类别型的。
'''
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.linalg import Vector, Vectors

df = spark.createDataFrame([
    (Vectors.dense(-1.0, 1.0, 1.0),),
    (Vectors.dense(-1.0, 3.0, 1.0),),
    (Vectors.dense(0.0, 5.0, 1.0),)], ["features"])
df.show()

indexer = VectorIndexer(inputCol="features", outputCol="indexed", maxCategories=2)
indexerModel = indexer.fit(df)

categoriesFeatures = indexerModel.categoryMaps.keys()
print("Choose" + str(len(categoriesFeatures)) +
     "categorical features:" + str(categoriesFeatures))
indexed = indexerModel.transform(df)
indexed.show()