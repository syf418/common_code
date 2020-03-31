# -*- coding: utf-8 -*-
# @Time: 2020/3/31 10:45
import warnings
warnings.filterwarnings(action='ignore')

import numpy as np
from fuzzywuzzy import fuzz
from numpy import array

from common_project.common_module.userDefinedError import dataTypeError

class text_similar():
    @staticmethod
    def _cosine_similarity(vector_a, vector_b):
        """
        Cosine similarity
        :param vector_a: 向量 a
        :param vector_b: 向量 b
        :return: sim
        """
        vector_a = np.mat(vector_a)
        vector_b = np.mat(vector_b)
        num = float(vector_a * vector_b.T)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        cos = num / denom
        cosSim = 0.5 + 0.5 * cos  # normalization
        return cosSim

    def __init__(self, text_a, text_b):
        self.text_a = text_a
        self.text_b = text_b

    def vector_similar(self, method="COS"):
        '''
        text_a, text_b are vectors!
        :param method: COS means "Cosine similarity"
        :return:
        '''
        if type(self.text_a) not in [list,array] or type(self.text_b) not in [list,array]:
            raise dataTypeError
        if method == "COS":
            similar = self._cosine_similarity(self.text_a, self.text_b)
        else:
            similar = None
        return similar

    def string_similar(self, method="MED"):
        '''
        text_a, text_b are strings!
        :param method: MED means "Minimum Edit Distance"
        :return:
        '''
        if type(self.text_a) is not str or type(self.text_b) is not str:
            raise dataTypeError
        if method == "MED":
            similar = fuzz.ratio(self.text_a, self.text_b) / 100
        else:
            similar = None
        return similar

if __name__ == "__main__":
    item_a = text_similar([3,5,7,1,0],[2,7,1,5,3])
    sim1 = item_a.vector_similar()
    print("sim1:", sim1)

    item_b = text_similar("在山腰间飘逸的风雨", "笑声盘旋半山腰")
    sim2 = item_b.string_similar()
    print("sim2:", sim2)





