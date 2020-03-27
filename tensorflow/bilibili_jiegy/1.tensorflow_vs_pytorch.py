# -*- coding: utf-8 -*-
'''
@Time    : 2019/12/25 22:28
@Author  : shangyf
@File    : 1.tensorflow_vs_pytorch.py
'''
# 1 + 1/2 + 1/2^2 + ... + 1/2^50
import warnings
warnings.filterwarnings(action='ignore')

import tensorflow as tf
print(tf.__version__)

x = tf.Variable(0.0)
y = tf.Variable(0.0)
print(x, y)

# x = x+y
add_op = x.assign(x+y)
# y = y/2
div_op = y.assign(y/2)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(50):
        sess.run(add_op)
        sess.run(div_op)
    print(x.eval())

# import torch