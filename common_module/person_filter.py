# -*- coding: utf-8 -*-
# @Time: 2020/6/4 9:34
# -*- coding: utf-8 -*-
# @Time: 2020/6/3 16:12
import warnings
warnings.filterwarnings(action='ignore')

from pandas import DataFrame
from matplotlib import pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示符号
sns.set_style('whitegrid',{'font.sans-serif':['Arial Unicode MS','Arial']})


def pearson_filter(df:DataFrame, keep_ratio, cal_cols=None, heatmap=True) -> list:
    '''
    根据皮尔逊相似度过滤字段
    :param df:
    :param keep_ratio: 保留率
    :param cal_cols: 参与计算的字段列表
    :param heatmap: 是否输出热力图
    :return:
    '''
    if cal_cols:
        df_cal = df[cal_cols]
        corr = df_cal.corr()
    else:
        corr = df.corr()

    # 筛选
    drop_col = []
    for i in range(len(cal_cols)):
        for j in range(i+1, len(cal_cols)):
            if corr.iloc[i][cal_cols[j]] >= keep_ratio:
                drop_col.append(cal_cols[j])
        drop_col = list(set(drop_col))
    keep_col = list(set(df.columns) - set(drop_col))

    if heatmap:
        # 热力图
        sns.heatmap(corr, center=2, annot=True)
        plt.savefig("corr.png")
        plt.show()

    return keep_col


