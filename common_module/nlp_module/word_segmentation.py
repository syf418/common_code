# -*- coding: utf-8 -*-
# @Time: 2020/3/30 13:20
import warnings
warnings.filterwarnings(action='ignore')

from pandas import DataFrame
from numpy import array
import jieba
from jieba import posseg
# jieba.enable_parallel() # parallel mode only supports posix system

from common_project.common_module.userDefinedError import NonSupportError

class word_segmentation():
    @staticmethod
    def _initial(userDictPath, stopKeyPath):
        if userDictPath:
            jieba.load_userdict(userDictPath)
        if stopKeyPath:
            try:
                with open(stopKeyPath, 'r', encoding='utf-8') as f_stop:
                    stopkey_list = f_stop.readlines()
            except:
                with open(stopKeyPath, 'r', encoding='gbk') as f_stop:
                    stopkey_list = f_stop.readlines()
            finally:
                stopkey_list = [i.strip("\n") for i in stopkey_list]
        else:
            stopkey_list = []
        return stopkey_list

    @staticmethod
    def _posseg_cut(x, stopkey_list=[], flag_options=[], return_flag=True):
        if return_flag:
            if len(flag_options) > 0:
                cut_result = [i.word + "-" + i.flag for i in list(posseg.cut(x))
                              if i.word not in stopkey_list and i.flag in flag_options]
            else:
                cut_result = [i.word + "-" + i.flag for i in list(posseg.cut(x)) if i.word not in stopkey_list]
        else:
            if len(flag_options) > 0:
                cut_result = [i.word for i in list(posseg.cut(x))
                              if i.word not in stopkey_list and i.flag in flag_options]
            else:
                cut_result = [i.word for i in list(posseg.cut(x)) if i.word not in stopkey_list]
        cut_result = " ".join(cut_result)
        return cut_result

    def __init__(self, datas, target_col='', userDictPath=None, stopKeyPath=None):
        self.datas = datas
        self.target_col = target_col
        self.stopkey_list = self._initial(userDictPath, stopKeyPath)

    def cut_to_words(self,  flag_options=[], return_flag=False):
        if type(self.datas) is str:
            self.datas = self._posseg_cut(self.datas, self.stopkey_list, flag_options, return_flag)
        elif type(self.datas) is DataFrame:
            self.datas["{}_cut".format(self.target_col)] = self.datas[self.target_col].apply(
                                lambda x: self._posseg_cut(x, self.stopkey_list, flag_options, return_flag))
        elif type(self.datas) in [list,array]:
            result = []
            for text in self.datas:
                result.append(self._posseg_cut(text, self.stopkey_list, flag_options, return_flag))
            self.datas = result
        else:
            raise NonSupportError
        return self.datas


if __name__ == "__main__":
    text = "我突然释怀的笑，笑声盘旋半山腰，随风在飘摇啊摇，来到我的面前摇"
    text_ = word_segmentation(text)
    s = text_.cut_to_words(return_flag=True, flag_options=["n","v"])
    print("s:", s)

    import pandas as pd
    df = pd.DataFrame(["我突然释怀的笑", "笑声盘旋半山腰", "随风在飘摇啊摇", "来到我的面前摇"], columns=["text"])
    text_ = word_segmentation(df, "text")
    s2 = text_.cut_to_words(return_flag=True)
    print("s2:", s2)
