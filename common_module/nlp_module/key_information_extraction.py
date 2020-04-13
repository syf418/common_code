# -*- coding: utf-8 -*-
# @Time: 2020/4/13 15:17
import warnings
warnings.filterwarnings(action='ignore')

from textrank4zh import TextRank4Sentence, TextRank4Keyword
import textrank4zh
import sys
sys.path.append("../../common_module/")

from userDefinedError import NonSupportError

class key_information_extraction():
    def __init__(self, text, mode):
        '''

        :param text:
        :param mode: 0 means keywords, 1 means keysentences
        '''
        self.text = text
        self.mode = mode

    def textRank(self, n=3, window=5, min_len=2, return_weight=True):
        result = []
        if self.mode == 0:
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=self.text, lower=True, window=window)
            for item in tr4w.get_keywords(n, word_min_len=min_len):
                if return_weight:
                    result.append((item['word'], item['weight']))
                else:
                    result.append(item['word'])
        elif self.mode == 1:
            # attention: 此处修改原代码设定增加分割符
            textrank4zh.util.sentence_delimiters.extend([",","，"])
            tr4s = TextRank4Sentence()
            tr4s.analyze(text=self.text, lower=True, source='no_stop_words')
            for item in tr4s.get_key_sentences(num=n, sentence_min_len=min_len):
                if return_weight:
                    result.append((item['sentence'], item['weight']))
                else:
                    result.append(item['sentence'])
        else:
            raise NonSupportError
        return result

if __name__ == "__main__":
    text = "你发如雪，凄美了离别，我焚香感动了谁，邀明月让回忆皎洁，爱在月光下完美"
    infor_extra = key_information_extraction(text, 0)
    r = infor_extra.textRank(return_weight=True)
    print("r:", r)
