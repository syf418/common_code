# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/26 23:48
@Author  : shangyf
@File    : 3.tf_keras回调函数.py
'''
import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

import tensorflow as tf
import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import datetime

fashion_mnist = keras.datasets.fashion_mnist
(x_train_all, y_train_all), (x_test, y_test) = fashion_mnist.load_data()
x_valid, x_train = x_train_all[:5000], x_train_all[5000:]
y_valid, y_train = y_train_all[:5000], y_train_all[5000:]


# 归一化：x = (x -u) / std
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(
    x_train.astype(np.float32).reshape(-1,1)).reshape(-1, 28, 28)
x_valid_scaled = scaler.transform(
    x_valid.astype(np.float32).reshape(-1, 1)).reshape(-1,28,28)
x_test_scaled = scaler.transform(
    x_test.astype(np.float32).reshape(-1,1)).reshape(-1,28,28)

# tf.keras.Sequential
model = keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape=[28,28]))
# 批归一化
model.add(keras.layers.BatchNormalization())
'''
激活函数在批归一化之前或之后的考虑
放在之前的写法：
    model.add(keras.layers.Dense(100))
    model.add(keras.layes.BatchNormalization())
    model.add(keras.layers.Activation('relu'))
'''
model.add(keras.layers.Dense(300, activation="relu"))
# 添加dropout
model.add(keras.layers.AlphaDropout(rate=0.5))
model.add(keras.layers.Dense(100, activation="selu"))
model.add(keras.layers.Dense(10, activation="softmax"))

'''
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[28,28]),
    keras.layers.Dense(300, activation='relu'),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
'''

# relu: y=max(0, x)
# softmax: 将向量变成概率分布， x = [x1, x2, x3]
#       y = [e^x1/sum, e^x2/sum, e^x3/sum]  sum = e^x1 + e^x2 +e^x3

# reason for sparse: y->index, y->one_hot->[]
model.compile(loss="sparse_categorical_crossentropy",
              optimizer='sgd', metrics=["accuracy"])

print(model.layers)
print(model.summary())

# !!! Tensorboard, earlystopping, ModelCheckpoint
logdir = './calbacks'
if not os.path.exists(logdir):
    os.mkdir(logdir)
output_model_file = os.path.join(logdir,
                                 "fashin_mnist_model.h5")
callbacks = [
    tf.keras.callbacks.TensorBoard(logdir),
    tf.keras.callbacks.ModelCheckpoint(output_model_file,
                                       save_best_only=True),
    tf.keras.callbacks.EarlyStopping(patience=5, min_delta=1e-3)
]
history = model.fit(x_train_scaled, y_train, epochs=10,
                    callbacks=callbacks,
          validation_data=(x_valid_scaled, y_valid))
print("history:", type(history), history.history)

def plot_learning_curves(history):
    pd.DataFrame(history.history).plot(figsize=(8, 5))
    plt.grid(True)
    plt.gca().set_ylim(0, 1)
    plt.show()

plot_learning_curves(history)

print(model.evaluate(x_test_scaled, y_test))

# tensorboard
'''
用tree指令查看文件夹，打开tensorboard:
    tensorboard --logdir=callbacks
本地网址：localhost:6006
'''