# -*- coding: utf-8 -*-
# @Time: 2020/2/10 14:43
import warnings
warnings.filterwarnings(action="ignore")

import datetime
import time

class show_time():
    _start = time.time()
    _start_ori = time.time()
    def __init__(self):
        ...

    def _now(self, describe="The Now"):
        print("{}:".format(describe), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), flush=True)

    def _restart(self):
        self._start = time.time()

    def _spend_time(self, module_name=''):
        end = time.time()
        spend_s = round(end - self._start, 2)
        spend_m = round(spend_s / 60, 2)
        spend_h = round(spend_m / 60, 2)
        print("{} spend time: {} s = {} m = {} h".format(module_name, spend_s, spend_m, spend_h), flush=True)

    def _all_spend_time(self):
        end = time.time()
        spend_s = round(end - self._start_ori, 2)
        spend_m = round(spend_s / 60, 2)
        spend_h = round(spend_m / 60, 2)
        print("All spend time: {} s = {} m = {} h".format(spend_s, spend_m, spend_h), flush=True)


if __name__ == "__main__":
    time_class = show_time()
    time_class._now()
    time.sleep(5)
    time_class._spend_time()
    time_class._restart()
    time.sleep(3)
    time_class._spend_time()
    time_class._all_spend_time()
    time_class._now()


