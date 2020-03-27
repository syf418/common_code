# -*- coding: utf-8 -*-
# @Time: 2020/3/9 13:28
import warnings
warnings.filterwarnings(action='ignore')

import os
import datetime
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号

def show_plot(index_list, true_values_list, pre_values_list, new_name=None):
    print("\t +++ plot show +++")
    plt.figure(figsize=(10, 6))
    plt.xlabel("时间")
    plt.ylabel("指标值")
    plt.xticks(rotation=90)
    plt.plot(index_list, true_values_list, c='b', label="True")
    plt.plot(index_list, pre_values_list,  c='r', label="Predict")
    plt.title("预测值图示")
    plt.legend()
    plt.grid()
    if not new_name:
        new_name = datetime.datetime.now().strftime("%Y%m%d%H%M")
    temp_path = "./temppics/"
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    plt.savefig(temp_path + "{}.png".format(new_name))
    plt.show()

def horizontal_bar_plot(index:list, values:list, max_num=10, title="水平横向的柱状图"):
    print("\t +++ Horizontal bar plot +++")
    index = index[:max_num]
    values = values[:max_num]
    index.reverse()
    values.reverse()
    fig, ax = plt.subplots()
    b = ax.barh(range(len(index)), values, color='#6699CC')
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y()+rect.get_height()/2, '%d' % int(w), ha='left', va='center')
    ax.set_yticks(range(len(index)))
    ax.set_yticklabels(index)
    plt.title(title, loc='center', fontsize='20', fontweight='bold', color='red')
    plt.show()


if __name__ == "__main__":
    #城市数据。
    city_name = ['北京', '上海', '广州', '深圳', '成都']
    values = [2,5,7,6,9]
    horizontal_bar_plot(city_name, values)
