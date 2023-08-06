# -*- coding: UTF-8 -*-
import datetime
import time


def date2timestamp_s(data_str, time_format="%Y-%m-%d %H:%M:%S"):
    """
    日期时间转换成秒级时间戳
    :param data_str: str，日期时间
    :param time_format: str，传入的日期时间的格式，默认是"%Y-%m-%d %H:%M:%S"
    :return:
    """
    datetime_mid = datetime.datetime.strptime(data_str, time_format)
    return int(time.mktime(datetime_mid.timetuple()))


def date2timestamp(data_str, time_format="%Y-%m-%d %H:%M:%S.%f"):
    """
    日期时间转换成毫秒级时间戳
    :param data_str: str，日期时间
    :param time_format: str，传入的日期时间的格式，默认是"%Y-%m-%d %H:%M:%S.%f"
    :return: int，时间戳
    """
    datetime_mid = datetime.datetime.strptime(data_str, time_format)
    return int(time.mktime(datetime_mid.timetuple())) * 1000 + int(round(datetime_mid.microsecond / 1000.0))


def timestamp2date(timestamp: int, time_format="%Y-%m-%d %H:%M:%S"):
    """
    时间戳转换为指定格式的日期
    :param timestamp: int，时间戳
    :param time_format: str，传入的日期时间的格式，默认是"%Y-%m-%d %H:%M:%S"
    :return:
    """
    # 传入的是毫秒级的时间戳
    if timestamp > 10 ** 10:
        timestamp = timestamp / 1000.0
    datetime_array = datetime.datetime.fromtimestamp(timestamp)
    return datetime_array.strftime(time_format)


def get_current_time(time_format="%Y-%m-%d %H:%M:%S"):
    """
    获取当前日期时间
    :param time_format: 输出的日期时间格式，默认是"%Y-%m-%d %H:%M:%S"，要显示毫秒"%Y-%m-%d %H:%M:%S.%f"
    :return:
    """
    return datetime.datetime.now().strftime(time_format)


def get_current_date(time_format="%Y-%m-%d"):
    """
    获取当前日期
    :param time_format: 输出的日期格式，默认是"%Y-%m-%d"
    :return:
    """
    return datetime.datetime.now().strftime(time_format)


def get_yesterday_date(time_format="%Y-%m-%d"):
    """
    获取昨天日期
    :param time_format: 输出的日期格式，默认是"%Y-%m-%d"
    :return:
    """
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    return yesterday.strftime(time_format)


def get_current_timestamp_s():
    """
    获取当前日期时间对应的时间戳（秒级）
    :return:
    """
    return int(time.time())


def get_current_timestamp_ms():
    """
    获取当前日期时间对应的时间戳（毫秒级）
    :return:
    """
    return int(round(time.time() * 1000))
