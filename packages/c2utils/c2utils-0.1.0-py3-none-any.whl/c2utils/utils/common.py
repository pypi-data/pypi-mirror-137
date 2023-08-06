# -*- coding: UTF-8 -*-
import configparser
import functools
import numbers
import random
import re
import string
import time


def calculate_execution_time(func):
    """
    计算程序执行时间装饰器
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        print('{} took {} ms'.format(func.__name__, (end - start) * 1000))
        return res

    return wrapper


def is_chinese(uchar):
    """
    判断一个字符是否是汉字
    :param uchar:
    :return:
    """
    if '\u4e00' <= uchar <= '\u9fa5' or '0' <= uchar <= '9' or ' ' == uchar:
        return True
    else:
        return False


def is_chinese_string(text):
    """
    判断输入文本是否全为汉字
    :param text:
    :return:
    """
    text = clear_all_punctuation(text)
    for c in text:
        if not is_chinese(c):
            return False
    return True


def is_zh(ch):
    """
    return True if ch is Chinese character.
    full-width puncts/latins are not counted in.
    :param ch:
    :return:
    """
    x = ord(ch)
    # CJK Radicals Supplement and Kangxi radicals
    if 0x2e80 <= x <= 0x2fef:
        return True
    # CJK Unified Ideographs Extension A
    elif 0x3400 <= x <= 0x4dbf:
        return True
    # CJK Unified Ideographs
    elif 0x4e00 <= x <= 0x9fbb:
        return True
    # CJK Compatibility Ideographs
    elif 0xf900 <= x <= 0xfad9:
        return True
    # CJK Unified Ideographs Extension B
    elif 0x20000 <= x <= 0x2a6df:
        return True
    else:
        return False


def is_zhs(text):
    """
    判断输入文本是否全为汉字
    :param text:
    :return:
    """
    for i in text:
        if not is_zh(i):
            return False
    return True


def is_digit(obj):
    """
    判断输入对象是否是数字
    :param obj:
    :return:
    """
    return isinstance(obj, (numbers.Integral, numbers.Complex, numbers.Real))


def is_number_in_string(text):
    """
    判断文本中是否含有数字
    :param text:
    :return:
    """
    return bool(re.search(r'\d', text))


def extract_numbers(text):
    """
    提取文本中的数字
    :param text:
    :return: <class 'list'>
    """
    return extract_text_through_re(r'\d+', text)


def clear_all_spaces(text):
    """
    去除文本中的所有空格
    :param text:
    :return:
    """
    return _replace_pattern(r' {1,}', "", text.strip())


def clear_all_punctuation(text):
    """
    去除文本中的标点符号
    :param text:
    :return:
    """
    return _replace_pattern(r'\W+', "", text.strip())


def is_alphabet_string(text):
    """
    判断输入文本是否全是英文
    :param text:
    :return:
    """
    text = clear_all_punctuation(text).lower()
    for c in text:
        if c < 'a' or c > 'z':
            return False
    return True


def is_alphabet(uchar):
    """
    判断一个字符是否是英文字母
    :param uchar:
    :return:
    """
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


def randomly_generate_string(n: int) -> str:
    """
    随机生成n位字符串
    :param n:
    :return:
    """
    return ''.join(random.sample(string.ascii_letters, n))


def _get_config(path):
    """
    读取配置文件（xx.ini）
    :param path:
    :return:
    """
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    return config


class ReadConfig:
    """
    读取配置文件类
    """

    def __init__(self, path):
        self.config = _get_config(path)

    def get_all_sections(self):
        """
        获取配置文件中所有section
        :return: <class 'list'>
        """
        return self.config.sections()

    def get_all_items(self, section):
        """
        获取名为section所对应的全部键值对
        :param section:
        :return: <class 'list'>
        """
        return self.config.items(section)

    def get_param(self, section, param):
        """
        获取section中param对应的值
        :param section:
        :param param:
        :return: <class 'str'>
        """
        return self.config.get(section, param)


def _replace_pattern(re_str, sub_str, text):
    """
    正则匹配
    :param re_str:
    :param sub_str:
    :param text:
    :return:
    """
    regex_pattern = re.compile(re_str)
    return regex_pattern.sub(sub_str, text)


def extract_text_through_re(re_str, text):
    """
    通过正则表达式抽取文本
    :param re_str: 正则表达式
    :param text: 待抽取的文本
    :return:
    """
    if text == '':
        return []
    return re.findall(re_str, text)


def _replace_chinese(text):
    """
    删除输入文本中的所有汉字
    :param text:
    :return:
    """
    return _replace_pattern(u'[\u4E00-\u9FA5]', r' ', text)
