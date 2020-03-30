# -*- coding: utf-8 -*-
# @Time: 2020/3/30 13:20
import warnings
warnings.filterwarnings(action='ignore')

from pandas import DataFrame
from numpy import array
import jieba

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
        else:
            stopkey_list = []
        return stopkey_list

    def __init__(self, datas, target_col=''):
        self.datas = datas
        self.target_col = target_col

    def cut_to_words(self, userDictPath=None, stopKeyPath=None):
        stopkey_list = self._initial(userDictPath, stopKeyPath)
        if type(self.datas) is str:
            self.datas = list(jieba.cut(self.datas))
        elif type(self.datas) is DataFrame:
            stopkey_list = [i.strip("\n") for i in stopkey_list]
            self.datas["{}_".format(self.target_col)] = self.datas[self.target_col].apply(
                                lambda x: [i for i in list(jieba.cut(x)) if i not in stopkey_list])
        elif type(self.datas) in [list,array]:
            result = []
            for text in self.datas:
                result.append([i for i in list(jieba.cut(text)) if i not in stopkey_list])
            self.datas = result
        else:
            raise NonSupportError
        return self.datas


if __name__ == "__main__":
    text = "我突然释怀的笑，笑声盘旋半山腰，随风在飘摇啊摇，来到我的面前摇"

    text_ = word_segmentation([text])
    s = text_.cut_to_words()
    print("s:", s)
