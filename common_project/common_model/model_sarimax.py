# -*- coding: utf-8 -*-
# @Time: 2020/3/9 10:54
import warnings
warnings.filterwarnings(action='ignore')

import pandas as pd
from pandas import DataFrame
import numpy as np

from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error

import sys

class model_sarimax():
    @staticmethod
    def _sorted(data, sort_col):
        data = data.sort_values(sort_col).reset_index()
        return data

    @staticmethod
    # 模型评估指标-mape
    def _mape(y_true, y_pred, drop_abnormal=True):
        if drop_abnormal:
            # 需优化
            check_ = [(y_true[i], i) for i in range(len(y_true))
                                if isinstance(y_true[i], (int,float)) and y_true[i] != 0]
            y_true = [i[0] for i in check_]
            index_list = [i[1] for i in check_]
            y_pred = [y_pred[i] for i in range(len(y_pred)) if i in index_list]
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    def __init__(self, data:DataFrame, time_col:str, target_col:str, features=[]):
        self.data = self._sorted(data, time_col)
        self.time_col = time_col
        self.target_col = target_col
        self.features = features

    def _train_test_split(self, n_predict):
        return self.data.iloc[:-n_predict], self.data.iloc[-n_predict:]

    def _endog_exog_data(self, n_predict, train, test):
        self.endog_data_train = train[self.target_col].values.tolist()
        if len(self.features) == 0:
            self.exog_data_train = None
            self.exog_data_test = None
        elif len(self.features) == 1:
            self.exog_data_train = train[self.features[0]].values.tolist()
            exog_data_test = [test[self.features[0]]]
            self.exog_data_test = np.array(exog_data_test).reshape(n_predict, -1).tolist()
        else:
            self.exog_data_train = train[self.features].values.tolist()
            self.exog_data_test = test[self.features].values.reshape(n_predict, -1).tolist()
        return (self.endog_data_train, self.exog_data_train, self.exog_data_test)

    def _update_data(self, i, f_generate_features):
        # 预测结果添加到训练数据中
        df_pre = self.test.iloc[i]
        df_pre[self.target_col] = self.yhat
        if f_generate_features:
            # 调用外部函数生成补充特征
            self.train = f_generate_features(self.train, self.yhat)
        else:
            self.train = self.train.append(df_pre)
        return self.train

    def train(self, n_predict, order=(2,1,2), seasonal_order=None, one_step=True, f_generate_features=None,
                    show_summary=True):
        self.train, self.test = self._train_test_split(n_predict)
        self.yhat_all = []
        if one_step:
            for i in range(n_predict):
                print("{} is predicting ~~~~".format(i+1))
                pre_data = self._endog_exog_data(n_predict, self.train, self.test)
                model = SARIMAX(endog=pre_data[0], exog=pre_data[1], order=order, seasonal_order=seasonal_order)
                model_fit = model.fit(disp=False)
                if len(self.features) == 0:
                    yhat = model_fit.forecast(steps=1, exog=pre_data[2])
                else:
                    yhat = model_fit.forecast(steps=1, exog=pre_data[2][i])
                self.yhat = yhat[0]
                self.yhat_all.append(self.yhat)
                self._update_data(n_predict, i, f_generate_features)  # 更新训练集
        else:
            pre_data = self._endog_exog_data(n_predict, self.train, self.test)
            model = SARIMAX(endog=pre_data[0], exog=pre_data[1], order=order, seasonal_order=seasonal_order)
            model_fit = model.fit(disp=False)
            self.yhat_all = model_fit.forecast(steps=n_predict, exog=pre_data[2])
        if show_summary:
            self._summary(model_fit)
        return self.yhat_all

    def evaluation(self):
        true_list = self.test[self.target_col].values
        pred_list = self.yhat_all
        mape = self._mape(y_true=true_list, y_pred=pred_list)
        mse = mean_squared_error(y_true=true_list, y_pred=pred_list)
        print("+++ evaluation result +++:\n\t mape: {},  mse: {}".format(mape, mse), flush=True)
        return mape, mse

    def _summary(self, model):
        summary = model.summary()
        self.__str__("summary", summary)

    def __str__(self, title, items):
        print("*****【{}】*****\n".format(title), items, flush=True)


if __name__ == "__main__":
    # load data
    df = pd.read_csv("../data_for_inc/data_with_time_features2_amend_new.csv", encoding='gbk')
    del df["level_0"]
    del df["index"]
    # print("cols:\n", df.columns.tolist())

    df = df[['time', 'complaints_new', 'logging_users',
             'date', 'hour', 'minute', 'weekday', 'month', 'dayofmonth',
             'logging_users_mean_14', 'logging_users_std_14',
             'logging_users_mean_7', 'logging_users_std_7',
             'abnormal', 'wantb',
             'complaints_new_mean_14', 'complaints_new_std_14',
             'complaints_new_mean_7', 'complaints_new_std_7']]

    # 配置区
    time_col = "time"
    target_col = "complaints_new"
    features = ['logging_users',
                'date', 'hour', 'minute', 'weekday', 'month', 'dayofmonth',
                'logging_users_mean_14', 'logging_users_std_14',
                'logging_users_mean_7', 'logging_users_std_7',
                'abnormal', 'wantb',
                'complaints_new_mean_14', 'complaints_new_std_14',
                'complaints_new_mean_7', 'complaints_new_std_7']


    def date_to_num(df, col):
        df[col] = df[col].apply(lambda x: int(str(x).replace("-", "")))
        return df

    df = date_to_num(df, "date")
    df["date"] = df["date"].astype(int)

    model_sarimax = model_sarimax(df[["time", "complaints_new"]], time_col, target_col, features=[])
    model_sarimax.train(n_predict=3, one_step=True, f_generate_features=False)
    model_sarimax.evaluation()
