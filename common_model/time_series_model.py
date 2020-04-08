# -*- coding: utf-8 -*-
# @Time: 2020/3/4 9:14
"""
Time series prediction model for single index
"""
import warnings
warnings.filterwarnings(action='ignore')

from pmdarima.arima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARIMA

import pandas as pd
from pandas import DataFrame
from common_project.common_module.userDefinedError import NonSupportError, NoResultsError

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
            raise NonSupportError()

        return self.model

    def train(self, n_predict, method='forecast'):
        """
        :param n_predict:
        :param method: 可选 forecast / predict
        :return:
        """
        print("--->: {} start training...".format(self.model_name), flush=True)
        if self.model_name == "auto_arima":
            if method == "forecast":
                self.yhat = self.model.predict(n_periods=n_predict).tolist()
            else:
                self.yhat = self.model.predict_in_sample(start=len(self.data), end=(len(self.data)+n_predict-1)).tolist()
        elif self.model_name == "arima":
            self.model_fit = model.fit(disp=-1)
            if method == "forecast":
                # 返回预测结果，标准误差和置信区间,这里只取预测结果
                self.yhat = self.model_fit.forecast(steps=n_predict)[0]
            else:
                raise NonSupportError()
                self.yhat = self.model_fit.predict(start=len(self.data), end=(len(self.data)+n_predict-1), dynamic=True)
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
            raise NoResultsError()
        return self.yhat


if __name__ == "__main__":
    df = pd.read_csv("../../data_for_inc/data_with_time_features2_amend_new.csv", encoding='gbk')
    df = df[df["time"] > '2019-10-15 00:00'].sort_values("time")
    df = df[["time", "complaints_new"]]

    # module test
    arima_module = arima_module(df.iloc[-50:], "time", "complaints_new")
    model = arima_module.choose_module("auto_arima")
    yhat = arima_module.train(1, method="forecast")
    print("yhat:", yhat)

    yhat = arima_module.train(1, method="predict")
    print("yhat:", yhat)


