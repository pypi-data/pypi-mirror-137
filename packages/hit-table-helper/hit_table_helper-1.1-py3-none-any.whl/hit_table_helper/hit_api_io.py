# -*- coding: utf-8 -*-
import json
from typing import Iterable

import grequests

api_address = 'https://wxfwdt.hit.edu.cn/app/bkskbcx/kbcxapp/getBkszkb'


def get_week_courses_req(uid: str, weekday: int, semester: str):
    r = grequests.post(url=api_address, data={
        'info': json.dumps({
            'gxh': uid,
            'zc': str(weekday),
            'xnxq': semester,
        })
    })
    # interest = r.json()['module']['data']
    return r


def from_iterable(it: Iterable, weekday, semester: str):
    reqs = [get_week_courses_req(hit_id, weekday, semester) for hit_id in it]
    res = grequests.map(reqs)
    for i in res:
        yield i
