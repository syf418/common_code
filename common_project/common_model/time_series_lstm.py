import warnings
warnings.filterwarnings(action='ignore')

import tensorflow as tf
tf.enable_eager_execution()

import matplotlib.pyplot as plt
# https://www.jianshu.com/p/88090a7895db

def display_datas(df, col_names):
    plt.figure(figsize=(24, 8))
    for i in range(len(col_names)):
        plt.subplot(len(col_names), 1, i+1)
        plt.plot(df[col_names[i]].values)
        plt.title(col_names[i], y=0.5, loc='right')
    plt.show()

# 1.Univariate:
def Univariate(n_steps, n_features):
    '''
    input为多个时间步， output为一个时间步的问题
    :param n_steps: 为输入的x每次考虑几个时间步
    :param n_features: 为每个时间步的序列数
    :return:
    data sample:
    X,          y
    10,20,30    40
    20,30,40    50
    ...
    '''
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
    model.add(tf.keras.layers.Dense(1))
    model.compile(optimizer='adam', loss='mse')

    return model

# 2.Multiple Input
def multiple_input(n_steps, n_features):
    '''
    input为多个序列， output为一个序列的问题
    :param n_steps: 为输入的x每次考虑几个时间步
    :param n_features:
    :return:
    data sample:
    in_seq1： [10, 20, 30, 40, 50, 60, 70, 80, 90]
    in_seq2： [15, 25, 35, 45, 55, 65, 75, 85, 95]
    out_seq： [in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))]
    '''
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
    model.add(tf.keras.layers.Dense(1))
    model.compile(optimizer='adam', loss='mse')

    return model

# 3.Multiple Parallel
def multiple_parallel(n_steps, n_features):
    '''
    input为多个序列， output也是多个序列为问题
    :param n_steps: 为输入的x每次考虑几个时间步
    :param n_features:
    :return:
    '''
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(50, activation='relu', return_sequences=True,
                                   input_shape=(n_steps, n_features)))
    # 注意return_sequences=True
    model.add(tf.keras.layers.Dense(n_features))
    model.compile(optimizer='adam', loss='mse')

    return model

# 4.Multi-Step
def multi_step(n_steps_in, n_features, n_steps_out):
    '''
    input为多个时间步， output也是多个时间步的问题
    :param n_steps_in: 为输入的x每次考虑几个时间步
    :param n_features: 为输出的y每次考虑几个时间步
    :param n_steps_out: 为输入有几个序列
    :return:
    '''
    func1 = True
    if func1:
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.LSTM(100, activation='relu', return_sequences=True,
                                       input_shape=(n_steps_in, n_features)))
        # 注意return_sequences=True
        model.add(tf.keras.layers.LSTM(100, activation='relu'))
        model.add(tf.keras.layers.Dense(n_steps_out))
        model.compile(optimizer='adam', loss='mse')
    else:
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.LSTM(100, activation='relu', input_shape=(n_steps_in, n_features)))
        model.add(tf.keras.layers.RepeatVector(n_steps_out))
        model.add(tf.keras.layers.LSTM(100, activation='relu', return_sequences=True))
        model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dense()))
        model.compile(optimizer='adam', loss='mse')

    return model

# 5.Multivariate Multi-Step
def multivariate_multi_step(n_steps_in, n_features, n_steps_out):
    '''
    input为多个序列，output为多个时间步的问题
    :param n_steps_in:为输入的x每次考虑几个时间步
    :param n_features:为输入有几个序列
    :param n_steps_out:为输出的y每次考虑几个时间步
    :return:
    '''
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(100, activation='relu', return_sequences=True,
                                   input_shape=(n_steps_in, n_features)))
    model.add(tf.keras.layers.LSTM(100, activation='relu'))
    model.add(tf.keras.layers.Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')

    return model

# 6.Multiple Parallel Input & Multi-Step Output
def multiple_parallel_input_and_multi_step_output(n_steps_in, n_features, n_steps_out):
    '''
    input为多个序列， output也是多个序列&多个时间步的问题
    :param n_steps_in: 为输入的x每次考虑几个时间步
    :param n_features: 为输入有几个序列
    :param n_steps_out: 为输出的y每次考虑几个时间步
    :return:
    '''
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(200, activation='relu',
                                   input_shape=(n_steps_in, n_features)))
    model.add(tf.keras.layers.RepeatVector(n_steps_out))
    model.add(tf.keras.layers.LSTM(200, activation='relu', return_sequences=True))
    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(n_steps_out)))
    model.compile(optimizer='adam', loss='mse')
    return model





