# -*- coding: utf-8 -*-
# @Time: 2020/3/8 12:40
import warnings
warnings.filterwarnings(action="ignore")

import datetime
from pandas import DataFrame
import pandas as pd
from pandas.tseries.offsets import Hour, Minute, Second

class time_process():
    def __init__(self, data:DataFrame, time_col, time_format="%Y-%m-%d %H:%M:%S"):
        self.data = data
        self.time_col = time_col
        self.time_format = time_format

    def time_formatted(self, keep_format="%Y-%m-%d %H:%M"):
        self.data[self.time_col] = self.data[self.time_col].apply(lambda x:
                                        datetime.datetime.strptime(str(x), self.time_format).strftime(keep_format))
        return self.data

    def add_extra_inf(self, time_format="%Y-%m-%d %H:%M", options=[]):
        temp_col = "time_"
        self.data['time_'] = pd.to_datetime(self.data[self.time_col], format=time_format)
        if len(options) == 0:
            self.data["date"] = self.data[temp_col].dt.date
            self.data["hour"] = self.data[temp_col].dt.hour
            self.data["minute"] = self.data[temp_col].dt.minute
            self.data['weekday'] = self.data[temp_col].dt.dayofweek
            self.data['month'] = self.data[temp_col].dt.month
            self.data['dayofmonth'] = self.data[temp_col].dt.day
        else:
            for v in options:
                if v == "d":
                    self.data["date"] = self.data[temp_col].dt.date
                elif v == "h":
                    self.data["hour"] = self.data[temp_col].dt.hour
                elif v == "min":
                    self.data["minute"] = self.data[temp_col].dt.hour
                elif v == "weekday":
                    self.data['weekday'] = self.data[temp_col].dt.dayofweek
                elif v == "month":
                    self.data["month"] = self.data[temp_col].dt.month
                elif v == "dayofmonth":
                    self.data['dayofmonth'] = self.data[temp_col].dt.day
        del self.data[temp_col]
        return  self.data

    def generate_time_list(self, start=None, end=None, periods=None, freq="1min", time_format="%Y-%m-%d %H:%M"):
        if len([i for i in [start, end, periods] if i != None]) < 2:
            raise ("Missing the necessary parameters!")
        else:
            time_list = pd.date_range(start=start, end=end, periods=periods, freq=freq).\
                                        strftime(time_format).tolist()
        return time_list

    def time_shift(self, shift_s=0, shift_m=0, shift_h=0):
        self.data[self.time_col] = pd.to_datetime(self.data[self.time_col])
        self.data[self.time_col] = self.data[self.time_col] + Hour(shift_h) + Minute(shift_m) + Second(shift_s)
        self.data[self.time_col] = self.data[self.time_col].astype(str)
        return self.data


