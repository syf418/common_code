# -*- coding: utf-8 -*-
# @Time: 2020/3/31 13:04
import warnings
warnings.filterwarnings(action='ignore')

from pandas import DataFrame
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import word2vec
from sklearn.externals import joblib
import time
import multiprocessing

from common_project.common_module.nlp_module.word_segmentation import word_segmentation

class word_embedding():
    @staticmethod
    def _word_segmentation(datas:DataFrame, text_col:str):
        seg = word_segmentation(datas, text_col)
        datas = seg.cut_to_words(return_flag=False)
        return datas

    @staticmethod
    def _vectorization(word_list, model):
        vector_list = []
        for word in word_list:
            try:
                vector_list.append(model[word])
            except:
                continue
        return vector_list

    @staticmethod
    def _makeDirs(path):
        if not os.path.exists(path):
            os.makedirs(path)

    _unique_id = int(time.time())

    def __init__(self, datas, target_col, cutted=False):
        self.target_col = target_col
        self.cutted = cutted
        if not cutted:
            self.datas = self._word_segmentation(datas, target_col)
            self.target_col = self.target_col + "_cut"
        else:
            self.datas = datas

    def tf_idf(self, model_path=None):
        Tfv = TfidfVectorizer()
        new_col = self.target_col + "_tfidf"
        Tfv_model = Tfv.fit(self.datas[self.target_col].values)
        self.datas[new_col] = Tfv_model.transform(self.datas[self.target_col].values)
        if model_path:
            self._makeDirs(model_path)
            joblib.dump(Tfv_model, model_path + "Tfidf_model_{}.model".format(self._unique_id))
        return self.datas, Tfv_model

    def word2vec(self, size=100, window=5, method=0, min_count=5, iter=5, model_path=None):
        '''
        :param size:
        :param window:
        :param method: 0 -> DBOW, 1 -> Skip-Gram
        :param min_count:
        :param iter:
        :param model_path:
        :return:
        '''
        # attention: every words should be an element in list, not split by space on string type!
        if not self.cutted:
            self.datas[self.target_col] = self.datas[self.target_col].apply(lambda x: x.split(" "))
        w2v_model = word2vec.Word2Vec(self.datas[self.target_col].values.tolist(),
                                  size=size, window=window, sg=method, min_count=min_count, iter=iter,
                                  workers=multiprocessing.cpu_count())
        if model_path:
            self._makeDirs(model_path)
            w2v_model.wv.save_word2vec_format(model_path + "word2vec_{}.bin".format(self._unique_id), binary=True)

        # vectorization
        self.datas["w2v_embedding"] = self.datas[self.target_col].apply(lambda x: self._vectorization(x, w2v_model))
        return self.datas, w2v_model

if __name__ == "__main__":
    import pandas as pd

    df = pd.DataFrame(["我突然释怀的笑,随风在飘摇啊摇,谁在用琵琶弹奏一曲东风破",
                       "我突然释怀的笑,笑声盘旋半山腰,花落人断肠，我心事，静静躺",
                       "随风在飘摇啊摇,我突然释怀的笑,在我地盘这你就得听我的",
                       "来到我的面前绕,笑声盘旋半山腰,从天台向下俯瞰暴力在原地打转",
                       "我突然释怀的笑,随风在飘摇啊摇,谁在用琵琶弹奏一曲东风破",
                       "我突然释怀的笑,笑声盘旋半山腰,花落人断肠，我心事，静静躺",
                       "随风在飘摇啊摇,我突然释怀的笑,在我地盘这你就得听我的",
                       "来到我的面前绕,笑声盘旋半山腰,从天台向下俯瞰暴力在原地打转",
                       "缓缓飘落的枫叶像思念，在山腰间飘逸的风雨"
                       ], columns=["text"])
    emb = word_embedding(df, "text")
    df_new, m = emb.tf_idf()
    print(df_new)

    data, w2v_model = emb.word2vec(min_count=1, window=5, iter=20)
    print("data:\n", data)
    # 其它应用：词相似度任务
    print("最相似：", w2v_model.most_similar(positive=['盘旋', '飘逸'], negative=['静静'], topn=1))
    print("找异类：", w2v_model.doesnt_match(['盘旋', '飘逸', '静静']))
    print("相似度比较：", w2v_model.similarity('我', '在'))



