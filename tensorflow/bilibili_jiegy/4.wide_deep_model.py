# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/28 6:50
@Author  : shangyf
@File    : 4.wide_deep_model.py
'''
# tf.keras.callbacks
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

# 函数式API 功能 f(x) = h(g(x))
input = keras.layers.Input(shape=x_train.shape[1:])
hidden1 = keras.layers.Dense(30, activation='relu')(input)
hidden2 = keras.layers.Dense(30, activation='relu')(hidden1)

concat = keras.layers.concatenate([input, hidden2])
output = keras.layers.Dense(1)(concat)

model = keras.models.Model(inputs=[input],
                           outputs=[output])
# 子类API
class WideDeepModel(keras.models.Model):
    def __init__(self):
        super(WideDeepModel, self).__init__()
        '''定义模型的层次'''
        self.hidden1_layer = keras.layers.Dense(30, activation='relu')
        self.hidden2_layer = keras.layers.Dense(30, activation='relu')
        self.output_layer = keras.layers.Dense(1)

    def call(self, input):
        '''完成模型的正向计算'''
        hidden1 = self.hidden1_layer(input)
        hidden2 = self.hidden2_layer(hidden1)
        concat = keras.layers.concatenate([input, hidden2])
        output = self.output_layer(concat)
        return  output

mdoel = WideDeepModel()
model.build(input_shape=[None, 8])

# 多输入
input_wide = keras.layers.Input(shape=[5])
input_deep = keras.layers.Input(shape=[6])
hidden1 = keras.layers.Dense(30, activation='relu')(input_deep)
hidden2 = keras.layers.Dense(30, activation='relu')(hidden1)
concat = keras.layers.concatenate([input_wide, hidden2])
output = keras.layers.Dense(1)(concat)
model = keras.models.Model(inputs=[input_wide, input_deep],
                           outputs=[output])
# 多输出
input_wide = keras.layers.Input(shape=[5])
input_deep = keras.layers.Input(shape=[6])
hidden1 = keras.layers.Dense(30, activation='relu')(input_deep)
hidden2 = keras.layers.Dense(30, activation='relu')(hidden1)
concat = keras.layers.concatenate([input_wide, hidden2])
output = keras.layers.Dense(1)(concat)
output2 = keras.layers.Dense(1)(hidden2)
model = keras.models.Model(inputs=[input_wide, input_deep],
                           outputs=[output, output2])

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
multi_input = False
if multi_input:
    x_train_scaled_wide = x_train_scaled[:,:5]
    x_train_scaled_deep = x_train_scaled[:,2:]
    x_valid_scaled_wide = x_valid_scaled[:,:5]
    x_valid_scaled_deep = x_valid_scaled[:,2:]
    x_test_scaled_wide = x_test_scaled[:,:5]
    x_test_scaled_deep = x_test_scaled[:,2:]
history = model.fit([x_train_scaled,],
                    [y_train, ], epochs=10,
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