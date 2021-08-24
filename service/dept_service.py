#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import Query
from model.dept import Department
from dao import crud


def add_dept(dept: Department):
    r"""
    添加部门，name必选，remark可选
    """
    dept_dict = dept.dict()
    columns = []
    values = []
    for k in dept_dict.keys():
        columns.append(k)
        values.append(dept_dict[k])
    return crud.insert_items("dept_inf", columns=columns, values=[values])


def remove_dept(name: str = Query(..., min_length=1, max_length=50)):
    r"""
    删除部门，以查询参数name唯一指定
    """
    return crud.delete_items('dept_inf', where={'name': name})


def get_dept(name: str = Query(..., min_length=1, max_length=50)):
    r"""
    获取部门的信息，以查询参数name唯一指定
    """
    return crud.select_items('dept_inf', columns=['name', 'remark'], where={'name': name})


def update_dept(dept: Department):
    r"""
    更新部门的信息，以传入的name唯一指定，可选修改name和remark
    """
    items = dept.dict(exclude_unset=True)
    return crud.update_items('dept_inf', items, where={'name': items['name']})
