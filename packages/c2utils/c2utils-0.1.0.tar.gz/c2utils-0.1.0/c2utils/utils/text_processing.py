# -*- coding: UTF-8 -*-
import re

import pypinyin
from pypinyin import pinyin

from c2utils.config.langconv import Converter
from c2utils.config.pinyin_list import pinyin_split_list


def simple2tradition(text):
    """
    将简体转换成繁体
    :param text:
    :return:
    """
    if not text.strip():
        return ''
    text = Converter('zh-hant').convert(text)
    # line = line.encode('utf-8')
    return text


def tradition2simple(text):
    """
    将繁体转换成简体
    :param text:
    :return:
    """
    if not text.strip():
        return ''
    text = Converter('zh-hans').convert(text)
    # line = line.encode('utf-8')
    return text


def get_homophones_by_char(input_char):
    """
    根据汉字取同音字
    :param input_char:
    :return:
    """
    result = []
    # CJK统一汉字区的范围是0x4E00-0x9FA5，也就是我们经常提到的20902个汉字
    for i in range(0x4e00, 0x9fa6):
        if pinyin([chr(i)], style=pypinyin.NORMAL)[0][0] == pinyin(input_char, style=pypinyin.NORMAL)[0][0]:
            result.append(chr(i))
    return result


def get_homophones_by_pinyin(input_pinyin):
    """
    根据拼音取同音字
    :param input_pinyin:
    :return:
    """
    result = []
    # CJK统一汉字区的范围是0x4E00-0x9FA5,也就是我们经常提到的20902个汉字
    for i in range(0x4e00, 0x9fa6):
        if pinyin([chr(i)], style=pypinyin.TONE2)[0][0] == input_pinyin:
            # TONE2: 中zho1ng
            result.append(chr(i))
    return result


def chinese2pinyin(chinese):
    """
    中文文本转拼音，例：我爱zhongguo -> woaizhongguo
    :param chinese:
    :return:
    """
    style = pypinyin.Style.NORMAL
    pinyin_list = pypinyin.lazy_pinyin(chinese, style=style)
    return "".join(pinyin_list)


def pinyin_split(input_pinyin, pinyin_table=pinyin_split_list, max_len=6):
    """
    拼音分割（例：woaizhongguo -> wo ai zhong guo）
    :param input_pinyin:
    :param pinyin_table: 拼音分割字典
    :param max_len:
    :return:
    """
    input_pinyin = input_pinyin.lower()
    pinyin_len = len(input_pinyin)
    result = []

    # 逆向匹配
    while True:
        matched = 0
        matched_word = ''
        if pinyin_len < max_len:
            max_len = pinyin_len
        for i in range(max_len, 0, -1):
            s = input_pinyin[(pinyin_len - i):pinyin_len]
            # 字符串是否在拼音表中
            if s in pinyin_table:
                matched_word = s
                matched = i
                break
        # 未匹配到拼音
        if len(matched_word) == 0:
            break
        else:
            result.append(s)
            input_pinyin = input_pinyin[:(pinyin_len - matched)]
            pinyin_len = len(input_pinyin)
            if pinyin_len == 0:
                break
    return result[::-1]


def text_split(text: str):
    """
    文章分句
    :param text:
    :return:
    """
    text = re.sub(r'([。！？\?])([^”’])', r'\1\n\2', text)  # 单字符断句符
    text = re.sub(r'(\.{6})([^”’])', r'\1\n\2', text)  # 英文省略号
    text = re.sub(r'(\…{2})([^”’])', r'\1\n\2', text)  # 中文省略号
    text = re.sub(r'([。！？\?][”’])([^，。！？\?])', r'\1\n\2', text)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    res = text.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可
    return res.split("\n")
