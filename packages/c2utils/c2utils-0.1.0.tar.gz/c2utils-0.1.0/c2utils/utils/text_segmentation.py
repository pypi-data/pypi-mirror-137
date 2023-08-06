# -*- coding: UTF-8 -*-
import codecs
import os

import jieba
import jieba.analyse
import jieba.posseg as pseg

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def load_user_dictionary(user_dict_file_path=os.path.join(BASE_DIR, 'config', 'vocabulary', 'user_dict.txt')):
    """
    加载用户自定义词典
    :param user_dict_file_path:
    :return:
    """
    jieba.load_userdict(user_dict_file_path)


class Segment(object):
    def __init__(self, stopwords_file_path=os.path.join(BASE_DIR, 'config', 'vocabulary', 'baidu_stopwords.txt')):
        self.stopwords = set()
        self.stopwords_file = stopwords_file_path
        self.read_in_stopwords()

    def read_in_stopwords(self):
        """
        加载停用词
        :return:
        """
        file = codecs.open(self.stopwords_file, 'r', 'utf-8')
        while True:
            line = file.readline()
            line = line.strip('\r\n')
            if not line:
                break
            self.stopwords.add(line)
        file.close()

    def cut(self, sentence, stopwords=True, cut_all=False):
        """
        分词
        :param sentence:
        :param stopwords:
        :param cut_all:
        :return:
        """
        seg_list = jieba.cut(sentence, cut_all)
        results = []
        for seg in seg_list:
            if stopwords and seg in self.stopwords:
                continue
            results.append(seg)

        return results

    def pseg_cut(self, sentence, stopwords=True):
        """
        词性标注
        :param sentence:
        :param stopwords:
        :return:
        """
        pseg_cut_list = pseg.cut(sentence)
        words = []
        flags = []
        for word, flag in pseg_cut_list:
            if stopwords and word in self.stopwords:
                continue
            words.append(word)
            flags.append(flag)
        return words, flags

    def cut_for_search(self, sentence, stopwords=True):
        """
        搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词
        :param sentence:
        :param stopwords:
        :return:
        """
        seg_list = jieba.cut_for_search(sentence)
        results = []
        for seg in seg_list:
            if stopwords and seg in self.stopwords:
                continue
            results.append(seg)

        return results

    def extract_keywords_through_tfidf(self, sentence, idf_path=None, top_k=20):
        """
        通过jieba的TF-IDF算法获取关键词
        :param idf_path:
        :param sentence:
        :param top_k:
        :return:
        """
        jieba.analyse.set_stop_words(self.stopwords_file)
        if idf_path:
            jieba.analyse.set_idf_path(idf_path)

        tags = jieba.analyse.extract_tags(sentence, top_k)
        return tags

    @staticmethod
    def extract_keywords_through_text_rank(sentence, top_k=20):
        """
        通过jieba的TextRank算法获取关键词
        :param sentence:
        :param top_k:
        :return:
        """
        text_rank = jieba.analyse.textrank(sentence, top_k)
        return text_rank
