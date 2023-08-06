# -*- coding: utf-8 -*-
def gongKeShiYanBan():
    """工科实验班

    :return:
    """
    prefix = '120L'
    suffix = '01'
    for i in range(1, 7):
        for j in range(1, 20):
            yield prefix + str(i).zfill(2) + str(j).zfill(2) + suffix


def yingCai():
    """英才（20级）

    :return:
    """
    prefix = '720361'
    for i in range(1, 10):
        for j in range(0, 20):
            yield prefix + str(i).zfill(2) + str(j).zfill(2)


def shuXue():
    """数院

    :return:
    """
    prefix = '120120'
    suffix = '01'
    for i in range(1, 20):
        yield prefix + str(i).zfill(2) + suffix


def wuLi():
    """物院

    :return:
    """
    prefix = '120111'
    suffix = '01'
    for i in range(1, 20):
        yield prefix + str(i).zfill(2) + suffix
