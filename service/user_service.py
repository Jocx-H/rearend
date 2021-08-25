#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 提供给前端的服务

from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Union
from model.user import User
from dao import crud


def get_user(d_name: str,
             where: Optional[Dict[str, Union[str, int, float]]] = None,
             limit: int = 20,
             skip: int = 0):
    r"""
    从数据层获取用户信息，再返回JSON
    """
    user_data = crud.select_items('user_inf', where=where, limit=limit, skip=skip)
    return JSONResponse(user_data)


def delete_user(d_name: str,
                where: Optional[Dict[str, Union[str, int, float]]] = None):
    r"""
    根据用户信息删除用户
    """
    return JSONResponse(crud.delete_items('user_inf', where=where))


def add_user(d_name: str,
             user: User):
    colums


def update_user(d_name: str,
                user: User):
    pass


# def limit(restrict: int = 20, data: list = None):
#     r"""
#     限制一次性传回前端的数据条目，一次性最多返回20条
#
#     Args:
#         restrict: 返回的数据条目个数，上限为20条
#         data: 数据条目列表
#     """
#     if data is None:
#         raise ValueError("[错误]：`data` 为空值")
#         # 这里应该返回一个状态码
#     restrict = min(restrict, len(data))
#     restrict = min(restrict, 20)
#     return data[0: restrict]
#
#
# def skip(num: int, data: list = None):
#     r"""
#     跳过前num个数据条目
#
#     Args:
#         num: 跳过的数据条目数量
#         data: 数据条目列表
#     """
#     if data is None:
#         raise ValueError("[错误]：`data` 为空值")
#         # 这里应该返回一个状态码
#     return data[num:]
