#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.user import User
from dao import crud
from typing import Optional, Dict, Union, List
from service.login_service import hash_password

# def is_admin(username: str):
#     r"""
#     判断是否为管理员账户
#     """
#     return False


def decode_info(info: dict):
    r"""
    将dict里面的内容全部解码成数据库接受的格式
    """
    enums = set(['sex', 'status'])
    times = set(['birthday', 'create_time'])
    special_strs = ['EmailStr', 'face_url', 'avatar_url']
    for i in info.keys():
        if info[i] is None:
            pass
        elif i in enums:
            info[i] = info[i].value
        elif i in times:
            info[i] = info[i].timestamp()
        elif i in special_strs:
            info[i] = str(info[i])
        assert type(info[i]) == str or type(info[i]) == int \
            or type(info[i]) == float or type(info[i] is None)
    return info


def add_user(user: User) -> str:
    r"""
    添加员工
    """
    user_dict = decode_info(user.dict())
    user_dict['password'] = hash_password(user_dict['password'])
    columns = []
    values = []
    for k in user_dict.keys():
        if user_dict[k] is not None:
            columns.append(k)
            values.append(user_dict[k])
    return crud.insert_items("user_inf", columns=columns, values=[values])


def remove_user(username: Optional[str]) -> str:
    r"""
    删除员工，以username为唯一指定目标
    """
    if username is None:
        return crud.delete_items('user_inf', where=None)
    else:
        return crud.delete_items('user_inf', where={'username': username})


def update_user(username: Optional[str], user: User) -> str:
    r"""
    更新员工的信息，以username为唯一指定目标
    """
    items = user.dict(exclude_unset=True)
    items = decode_info(items)
    if username is None:
        return crud.update_items('user_inf', items, where=None)
    else:
        return crud.update_items('user_inf', items, where={'username': username})


def get_user(where: Optional[Dict[str, Union[str, int, float]]],
             limit: Optional[int],
             skip: int) -> List[Dict[str, Union[str, int, float]]]:
    r"""
    获取员工的信息，提供三种查询模式：
        1. 从数据库第一条开始返回条目
        2. 根据username查询直接访问一位员工
        3. 返回符合where条件的员工
    """
    if where is None:
        return crud.select_items('user_inf', where=None, limit=limit, skip=skip)
    else:
        where = {k: v for k, v in where.items() if v is not None} # 去除字典中值为None的键
        where = decode_info(where)
        return crud.select_items('user_inf', where=where, limit=limit, skip=skip)
