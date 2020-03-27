# -*- coding: utf-8 -*-
'''
@Time    : 2020/1/2 14:38
@Author  : shangyf
@File    : 6.tensorflow基础API.py
'''
import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np

import platform
print(platform.python_version())

import tensorflow as tf
tf.enable_eager_execution()


print(tf.__version__)

# 常量
t = tf.constant([[1,2,3], [4,5,6]])
print(t)
print(t[:, 1:])
print(t[..., 1])

