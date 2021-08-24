#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 提供给前端的服务

from fastapi.responses import JSONResponse



def get_data(d_name: str, **kwargs):
    r"""
    获取数据的主服务。先从数据层接口里面访问数据，在进行处理

    Args:
        d_name: 数据库表单的名字
        kwargs: 服务的名字。里面的可选服务包含了
                 1. limit: 限制每次返回前端的数据条目，上限为20
                 2. skip: 跳过前若干条数据条目后再取数据
    """
    data = []  # 待处理的数据条目

    # 以下是从数据层取数据
    # key服务和where服务逻辑上不能共存
    # 所以两者分别检查
    if kwargs['key'] is not None:
        data = user_dao.get_from_db(d_name, key=kwargs['key'])
    elif kwargs['where'] is not None:
        data = user_dao.get_from_db(d_name, where=kwargs['where'])
    else:
        data = user_dao.get_from_db(d_name)

    if len(data) is 0:
        # return 一个空数据的错误代码
        pass

    # 进行子服务
    data = skip(kwargs['skip'], data) if kwargs['skip'] is not None else data
    data = limit(kwargs['limit'],
                 data) if kwargs['limit'] is not None else data

    return JSONResponse(data)


def delete_data(d_name: str, **kwargs):
    r"""
    根据需求删除数据条目

    Args:
        d_name: 数据库表单的名字
        kwargs: 按照主键删除还是按照类型删除，必填
                1. key: 按照主键删除
                2. where: 按照类型删除
    """
    if len(kwargs) is 0:
        # return 错误代码
        pass

    if kwargs['key'] is None:
        return user_dao.delete_to_db(d_name, kwargs['where'])
    elif kwargs['where'] is None:
        return user_dao.delete_to_db(d_name, kwargs['key'])


def limit(restrict: int = 20, data: list = None):
    r"""
    限制一次性传回前端的数据条目，一次性最多返回20条

    Args:
        restrict: 返回的数据条目个数，上限为20条
        data: 数据条目列表
    """
    if data is None:
        raise ValueError("[错误]：`data` 为空值")
        # 这里应该返回一个状态码
    restrict = min(restrict, len(data))
    restrict = min(restrict, 20)
    return data[0: restrict]


def skip(num: int, data: list = None):
    r"""
    跳过前num个数据条目

    Args:
        num: 跳过的数据条目数量
        data: 数据条目列表
    """
    if data is None:
        raise ValueError("[错误]：`data` 为空值")
        # 这里应该返回一个状态码
    return data[num:]
