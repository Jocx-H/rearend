#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.dept import Department
from dao import crud
from typing import Optional, Dict, List, Union
from api.utils import exception_handler
from fastapi.encoders import jsonable_encoder

@exception_handler
def add_dept(dept: Department) -> str:
    r"""
    添加部门，name必选，remark可选
    """
    assert dept.name is not None, "必须传入name"
    dept_dict = jsonable_encoder(dept)
    columns = []
    values = []
    for k in dept_dict.keys():
        if dept_dict[k] is not None:
            columns.append(k)
            values.append(dept_dict[k])
    return crud.insert_items("dept_inf", columns=columns, values=[values])


@exception_handler
def remove_dept(name: Optional[str]) -> str:
    r"""
    删除部门，以路径参数name唯一指定
    """
    if name is None:
        return crud.delete_items('dept_inf', where=None)
    else:
        return crud.delete_items('dept_inf', where={'name': name})


@exception_handler
def get_dept(name: Optional[str], limit: Optional[int], skip: int) -> List[Dict[str, Union[str, int, float]]]:
    r"""
    获取部门的信息，以路径参数name唯一指定，可以选择limit和skip
    """
    if name is None:
        return crud.select_items('dept_inf', columns=['name', 'remark'],
                                 where=None, limit=limit, skip=skip)
    else:
        return crud.select_items('dept_inf', columns=['name', 'remark'],
                                 where={'name': name}, limit=limit, skip=skip)


@exception_handler
def update_dept(name: Optional[str], dept: Department) -> str:
    r"""
    更新部门的信息，以传入的name唯一指定，可选修改name和remark
    """
    items = dept.dict(exclude_unset=True)
    if name is None:
        return crud.update_items('dept_inf', items, where=None)
    else:
        return crud.update_items('dept_inf', items, where={'name': name})
