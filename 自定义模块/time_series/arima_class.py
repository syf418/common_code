# -*- coding: utf-8 -*-
# @Time: 2020/3/4 9:14
import warnings
warnings.filterwarnings(action='ignore')

from pmdarima.arima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARIMA

import pandas as pd
from pandas import DataFrame
from matplotlib import pyplot as plt

from error_module import UnsupportedError

class arima_module():
    def __init__(self, data:DataFrame, time_col, target_col):
        self.data = data[target_col].values
        self.time_col = time_col
        self.target_col = target_col

    def choose_module(self, model_name="auto_arima", P=2, D=1, Q=2, Period=7, seasonal_order=(0,0,0,7),
                      enforce_stationarity=True, enforce_invertibility=True):
        self.model_name = model_name
        if self.model_name == "auto_arima":
            self.model = auto_arima(self.data,start_p=1, start_q=1, max_p=P, max_q=Q, max_d=D,
                                    m=Period, error_action='ignore', trace=False)
        elif self.model_name == "arima":
            self.model = ARIMA(self.data, order=(P, D, Q))

        elif self.model_name == "sarimax":
            self.model = SARIMAX(endog=self.data, order=(P, D, Q), seasonal_order=seasonal_order,
                                 enforce_stationarity=True, enforce_invertibility=True)
        else:
            raise ("The model doesn't exist!")

        return self.model

    def train(self, n_predict, method='forecast'):
        """
        :param n_predict:
        :param method: 可选 forecast / predict
        :return:
        """
        print("--->: {} start training...".format(self.model_name), flush=True)
        if self.model_name == "auto_arima":
            self.model_fit = self.model
            if method == "forecast":
                self.yhat = self.model_fit.predict(n_periods=n_predict).tolist()
            else:
                self.yhat = self.model_fit.predict_in_sample(start=len(self.data), end=(len(self.data)+n_predict-1)).tolist()
        elif self.model_name == "arima":
            self.model_fit = model.fit(disp=-1)
            if method == "forecast":
                # 返回预测结果，标准误差和置信区间,这里只取预测结果
                self.yhat = self.model_fit.forecast(steps=n_predict)[0]
            else:
                raise UnsupportedError
                # self.yhat = self.model_fit.predict(start=len(self.data), end=(len(self.data)+n_predict-1), dynamic=True)
                # 需要进行预测结果还原
                '''
                对预测出来的数据，进行逆差分操作（由原始数据取对数后的数据加上预测出来的数据），然后再取指数即可还原。
                (待补充)
                '''

        elif self.model_name == "sarimax":
            self.model_fit = model.fit(disp=-1)
            if method == "forecast":
                self.yhat = self.model_fit.forecast(steps=n_predict)
            else:
                self.yhat = self.model_fit.predict(start=len(self.data), end=(len(self.data)+n_predict-1))
        else:
            raise ("The model doesn't exist!")
        return self.yhat

    def summary(self):
        print("summary:\n", self.model_fit.summary())
        return self.model_fit.summary()

    # def


def stationarity(data:DataFrame, diff=1, show_plot=False):
    """差分平稳化"""
    for i in range(diff):
        data = data.diff(1)
        if show_plot:
            plt.figure(figsize=(10,6))
            plt.plot(data.index, data.values)
            plt.title("diff {}".format(i+1))
            plt.grid()
            plt.show()
    return data



if __name__ == "__main__":
    import numpy as np

    df = pd.DataFrame()
    df["time"] = pd.date_range(start="2020-01-01 00:00", periods=100, freq="1min")
    df["y"] = np.random.rand(len(df))

    stationarity(df["y"], 3, True)

    # module test
    arima_module = arima_module(df.iloc[-50:], "time", "y")
    model = arima_module.choose_module("sarimax")
    yhat = arima_module.train(3, method="forecast")
    print("yhat:", yhat)

    yhat = arima_module.train(3, method="predict")
    print("yhat:", yhat)

    arima_module.summary()


