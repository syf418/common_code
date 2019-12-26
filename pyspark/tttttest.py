# -*- coding: utf-8 -*-
'''
@Time    : 2019/6/12 15:53
@Author  : shangyf
@File    : tttttest.py
'''
import pandas as pd
import numpy as np

if __name__ == "__main__":
    df = pd.DataFrame([['1','2','3'],['4','5','6']], columns=['a', 'b', 'c'])
    print(df['a'].iloc[0])
    df['a'] = df['a'].values.astype(np.float)
    print(type(df['a'].iloc[0]), df['a'].iloc[0])
    print(df['a'].index.tolist())