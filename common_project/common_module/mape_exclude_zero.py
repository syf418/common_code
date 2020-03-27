# -*- coding: utf-8 -*-
# @Time: 2020/3/23 15:49
import warnings
warnings.filterwarnings(action='ignore')

import numpy as np

def mape_exclude_zero(y_true, y_pred, drop_abnormal=True):
    n = len(y_true)
    if drop_abnormal:
        # 需优化
        check_ = [(y_true[i], i) for i in range(len(y_true))
                  if isinstance(y_true[i], (int, float)) and y_true[i] != 0]
        y_true = [i[0] for i in check_]
        index_list = [i[1] for i in check_]
        y_pred = [y_pred[i] for i in range(len(y_pred)) if i in index_list]
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    zero_nums = n - len(y_true)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100, (n, zero_nums, round(zero_nums/n, 3))

