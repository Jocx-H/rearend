#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.dept import Department
from dao import crud


async def add_dept(dept: Department):
    r"""
    添加部门，name必选，remark可选
    """
    # dept_service.add_dept
    return dept


async def remove_dept(name: str):
    r"""
    删除部门，以name唯一指定
    """
    # return dept_service.remove_dept()
    return name


async def get_dept(name: str):
    r"""
    获取部门的信息数据，以name唯一指定
    """
    # 1.通过调用相应的服务得到对应的反馈
    # return dept_service.get_dept_infos(name)
    return name


async def update_dept(dept: Department):
    r"""
    更新部分，以name唯一指定，可选修改name和remark
    """
    # dept_service.update_dept
    return dept
