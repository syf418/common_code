# -*- coding: utf-8 -*-
# @Time: 2020/3/8 11:16
import warnings
warnings.filterwarnings(action="ignore")

import time
import datetime

class show_time():
    __start = time.time()
    __start_ori = time.time()

    @staticmethod
    def _now():
        print("Time Now:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), flush=True)

    @staticmethod
    def _diff_value(m, n):
        spend_s = round(m/60, 2)
        spend_m = round(spend_s/60, 2)
        spend_h = round(spend_m/60, 2)
        return (spend_s, spend_m, spend_h)

    def __init__(self):
        self._now()

    def reset_start(self):
        self.__start = time.time()
        return self.__start

    def module_spend_time(self, module_name=''):
        end = time.time()
        s_ = end - self.__start
        self._spend = self._diff_value(s_, 2)
        self.__str__(module_name)
        self._now()
        return self._spend

    def all_spend_time(self, module_name='all'):
        end = time.time()
        s_ = end - self.__start_ori
        self._spend = self._diff_value(s_, 2)
        self.__str__(module_name)
        self._now()
        return self._spend

    def __str__(self, module_name):
        print("\t {} spend time: {} s = {} m = {} h".format(
                    module_name, self._spend[0], self._spend[1], self._spend[2]), flush=True)

if __name__ == "__main__":
    show_time = show_time()
    time.sleep(3)
    show_time.module_spend_time("module 1")
    show_time.reset_start()
    time.sleep(5)
    show_time.module_spend_time("module 2")

    show_time.all_spend_time("all")








