# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/29 15:57
@Author  : shangyf
@File    : 5.超参数搜索.py
'''
import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import os
import sys
import time
import tensorflow as tf
from tensorflow import keras

print(tf.__version__)
print(sys.version_info)
for module in mpl, np, pd, sklearn, tf, keras:
    print(module.__name__, module.__version__)

from sklearn.datasets import fetch_california_housing
housing = fetch_california_housing()

print(housing.DESCR)
print(housing.data.shape)
print(housing.target.shape)

from sklearn.model_selection import train_test_split

x_train_all, x_test, y_train_all, y_test = \
    train_test_split(housing.data, housing.target, random_state=418)
x_train, x_valid, y_train, y_valid = \
    train_test_split(x_train_all, y_train_all, random_state=418)
print(x_train.shape, y_train.shape)
print(x_valid.shape, y_valid.shape)
print(x_test.shape, y_test.shape)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_valid_scaled = scaler.transform(x_valid)
x_test_scaled = scaler.transform(x_test)

# learning_rate: [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2]
# W = W + grad * learning_rate

# 1.手动搜索
learning_rates = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2]
histories = []
for lr in learning_rates:
    model = keras.models.Sequential([
        keras.layers.Dense(30, activation="relu", input_shape=x_train.shape[1:]),
        keras.layers.Dense(1)
    ])
    optimizer = keras.optimizers.SGD(lr)

    model.compile(loss="mean_squared_error", optimizer=optimizer)
    callbacks = [keras.callbacks.EarlyStopping(patience=5, min_delta=1e-2)]

    history = model.fit(x_train_scaled, y_train,
                        validation_data=(x_valid_scaled, y_valid),
                        epochs=100,
                        callbacks = callbacks)
    histories.append(history)

def plot_learning_curves(history):
    pd.DataFrame(history.history).plot(figsize=(8, 5))
    plt.gca().set_ylim(0, 1)
    plt.show()
for lr, history in zip(learning_rates, histories):
    print("Learning rate:", lr)
    plot_learning_curves(history)

# 2.sklearn 超参数搜索
# RandomizedSearchCV
# -1.转化为sklearn的model
# -2.定义参数集合
# -3.搜索参数

def build_model(hidden_layers=1,
                layer_size=30,
                learning_rate=3e-3):
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(layer_size, activation="relu"),
              input_shape=x_train.shape[1:]),
    for _ in range(hidden_layers - 1):
        model.add(keras.layers.Dense(layer_size, activation='relu'))
    model.add(keras.layers.Dense(1))
    optimizer = keras.optimizers.SGD(learning_rate)
    model.compile(loss='mse', optimizer=optimizer)
    return model

sklearn_model = keras.wrappers.scikit_learn.KerasRegressor(build_model)
history = sklearn_model.fit(x_train_scaled, y_train, epochs=100,
                  validation_data = (x_valid_scaled, y_valid),
                  callbacks = callbacks)
plot_learning_curves(history)

# 参数集合
from scipy.stats import reciprocal
print(reciprocal.rvs(1e-4, 1e-2, size=10))

import numpy as np
# f（x）= 1/(x*log(b/a)), a <= x <= b
param_distribution = {
    "hidden_layers":[1,2,3,4],
    "layer_size": np.arange(1,100),
    "learning_rate": reciprocal(1e-4, 1e-2)}

from sklearn.model_selection import RandomizedSearchCV
random_search_cv = RandomizedSearchCV(
    sklearn_model,
    param_distribution,
    n_iter=10, # 表示从参数空间里sample多少个参数集合
    n_jobs=1,  # 并行处理数
    cv=5
)
random_search_cv.fit(x_train_scaled, y_train, epochs=100,
                     validation_data = (x_valid_scaled, y_valid),
                     callbacks=callbacks)
print(random_search_cv.best_params_)
print(random_search_cv.best_score_)
print(random_search_cv.best_estimator_)

model = random_search_cv.best_estimator_.model
model.evaluate(x_test_scaled, y_test)