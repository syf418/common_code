# -*- coding: utf-8 -*-
# @Time: 2020/3/30 8:57
import warnings
warnings.filterwarnings(action='ignore')

import re
from numpy import array
from fuzzywuzzy import process
import numpy as np

from common_project.common_module.userDefinedError import NonSupportError

class information_matching():
    def __init__(self, datas: array or list):
        self.datas = datas

    def keywords_matching(self, keywords:str or list, mode="and"):
        '''
        :param keywords:
        :param mode: "or" or "and"
        :return:
        '''
        result = []
        if type(keywords) is str:
            for text in self.datas:
                if re.findall(keywords, text):
                    result.append(text)
        elif type(keywords) is list:
            keywords_new = "|".join(keywords)
            for text in self.datas:
                if mode == "and":
                    if sorted(set(re.findall(keywords_new, text))) == sorted(keywords):
                        result.append(text)
                elif mode == "or":
                    list_ = re.findall(keywords_new, text)
                    if list_:
                        result.append((text, len(list_)))
                else:
                    raise NonSupportError
            result = sorted(result, key=lambda x:x[1], reverse=True)
        else:
            raise NonSupportError
        return result

    def fuzzy_matching(self, keywords:str or list, limit=1,return_score=False):
        '''
        Base on Levenshtein Distance(Edit Distance).
        :param keywords:
        :return:
        '''
        result = []
        if type(keywords) is str:
            result = process.extractBests(keywords, self.datas, limit=limit)
        elif type(keywords) is list:
            keywords_new = "".join(keywords)
            result = process.extractBests(keywords_new, self.datas, limit=limit)
        else:
            raise NonSupportError
        if not return_score:
            result = [i[0] for i in result]
        return result

if __name__ == "__main__":
    datas = np.array(["第几个一百天", "第十个一百天", "谁的一百天百天第一", "第几个两百天", "谁呀"])
    matching = information_matching(datas)
    r = matching.keywords_matching(["第一","百天"], mode="or")
    print("r:", r)
    r2 = matching.fuzzy_matching("谁一百天")
    print("r:", r2)

