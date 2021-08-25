#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.dept import Department
from dao import crud
from typing import Optional


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


def remove_dept(name: Optional[str]):
    r"""
    删除部门，以路径参数name唯一指定
    """
    if name is None:
        return crud.delete_items('dept_inf', where=None)
    else:
        return crud.delete_items('dept_inf', where={'name': name})


def get_dept(name: Optional[str], limit: Optional[int], skip:int):
    r"""
    获取部门的信息，以路径参数name唯一指定，可以选择limit和skip
    """
    if name is None:
        return crud.select_items('dept_inf', columns=['name', 'remark'],
                                 where=None, limit=limit, skip=skip)
    else:
        return crud.select_items('dept_inf', columns=['name', 'remark'],
                                 where={'name': name}, limit=limit, skip=skip)
    


def update_dept(name:Optional[str], dept: Department):
    r"""
    更新部门的信息，以传入的name唯一指定，可选修改name和remark
    """
    items = dept.dict(exclude_unset=True)
    if name is None:
        return crud.update_items('dept_inf', items, where=None)
    else:
        return crud.update_items('dept_inf', items, where={'name': name})
