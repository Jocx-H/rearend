#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.user import User
from dao import crud
from typing import Optional, Dict, Union

WRONG = 0


# def is_admin(username: str):
#     r"""
#     判断是否为管理员账户
#     """
#     return False


def decode_info(info: dict):
    r"""
    将dict里面的内容全部解码
    """
    enums = [
        'sex', 'status'
    ]

    times = [
        'birthday', 'create_date'
    ]

    url = [
        'face_url'
    ]

    for i in enums:
        info[i] = info[i].value
    for i in times:
        info[i] = str(info[i])
    for i in url:
        info[i] = str(info[i])
    return info


def add_user(user: User):
    r"""
    添加员工
    """
    user_dict = user.dict()
    user_dict = decode_info(user_dict)
    columns = list(user_dict.keys())
    values = list(user_dict.values())
    return crud.insert_items("user_inf", columns=columns, values=[values])


def remove_user(username: Optional[str]):
    r"""
    删除员工，以username为唯一指定目标
    """
    if username is None:
        return crud.delete_items('user_inf', where=None)
    else:
        return crud.delete_items('user_inf', where={'username': username})


def update_user(username: Optional[str], user: User):
    r"""
    更新员工的信息，以username为唯一指定目标
    """
    items = user.dict(exclude_unset=True)
    items = decode_info(items)
    if username is None:
        return crud.update_items('user_inf', items, where=None)
    else:
        return crud.update_items('user_inf', items, where={'username': username})


def get_user(username: Optional[str],
             where: Optional[Dict[str, Union[str, int, float]]],
             limit: Optional[int],
             skip: Optional[int]):
    r"""
    获取员工的信息，提供三种查询模式：
        1. 从数据库第一条开始返回条目
        2. 根据username查询直接访问一位员工
        3. 返回符合where条件的员工
    """
    if username is not None and where is None:
        return crud.select_items('user_inf', where={'username': username}, limit=limit, skip=skip)
    elif username is None and where is not None:
        return crud.select_items('user_inf', where=where, limit=limit, skip=skip)
    elif username is not None and where is not None:
        return crud.select_items('user_inf', limit=limit, skip=skip)
    else:
        return WRONG