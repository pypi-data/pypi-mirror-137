#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/27 5:53 PM
# @Author  : chenDing
import time
from datetime import datetime, timedelta
from collections import namedtuple


def _add_hour_min_sec(result_list, nt):
    new_res = []
    len_l = len(result_list)
    for index in range(len_l - 1):
        start_time = f"{result_list[index]} 00:00:00"
        end_time = f"{result_list[index + 1]} 00:00:00"
        new_res.append(nt(start_time, end_time))
    return new_res


def create_date_range(start_time, end_time):
    """
    生成规定天数内的时间间隔
    start_time： %Y-%m-%d
    end_time： %Y-%m-%d
    """
    result_list = []
    nt = namedtuple('day_start_to_end', ["start_time", "end_time"])
    sta_day = datetime.strptime(start_time, '%Y-%m-%d')
    end_day = datetime.strptime(end_time, '%Y-%m-%d')
    dlt_day = (end_day - sta_day).days + 2
    for i in range(dlt_day):
        tmp_day = sta_day + timedelta(days=i)
        tmp_day_txt = tmp_day.strftime('%Y-%m-%d')
        result_list.append(tmp_day_txt)
    return _add_hour_min_sec(result_list, nt)


def str2timestamp(time_string):
    """"""
    return time.mktime(time.strptime(time_string, '%Y-%m-%d %H:%M:%S'))


def timestamp2str(timestamp):
    """"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


if __name__ == '__main__':
    print(create_date_range('2020-1-1', '2020-1-2'))
