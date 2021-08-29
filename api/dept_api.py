#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Query, Path
from model.dept import Department
from model.code import Code400
from service import dept_service
from typing import Optional

# 构建api路由
router = APIRouter(
    prefix="/dept",
    tags=["Department"],
)


@router.post("/add", responses={400: {"model": Code400}})
async def add_dept(dept: Department):
    r"""
    添加部门，name必选，remark可选
    """
    return dept_service.add_dept(dept)



@router.delete("/remove-all", responses={400: {"model": Code400}})
async def remove_all_depts():
    r"""
    删除所有部门
    注意在删除部门时要保证没有员工在这个职位，否则无法删除
    """
    return dept_service.remove_dept(None)


@router.delete("/remove/{name}", responses={400: {"model": Code400}})
async def remove_dept(name: str = Path(..., min_length=1, max_length=50)):
    r"""
    删除部门，以路径参数name唯一指定
    注意在删除部门时要保证没有员工在这个职位，否则无法删除
    """
    return dept_service.remove_dept(name)


@router.get("/get-all", responses={400: {"model": Code400}})
async def get_all_depts(limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取所有部门的信息
    可以选择limit和skip
    """
    return dept_service.get_dept(None, limit, skip)


@router.get("/get/{name}", responses={400: {"model": Code400}})
async def get_dept(name: str = Path(..., min_length=1, max_length=50),
                   limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取部门的信息，以路径参数name唯一指定
    可以选择limit和skip
    """
    return dept_service.get_dept(name, limit, skip)


@router.put("/update-all", responses={400: {"model": Code400}})
async def update_all_depts(dept: Department):
    r"""
    更新部门的信息，以传入的路径参数name唯一指定(若不指定则更新所有部门)
    可选修改name和remark
    """
    return dept_service.update_dept(None, dept)


@router.put("/update/{name}", responses={400: {"model": Code400}})
async def update_dept(dept: Department,
                      name: str = Path(..., min_length=1, max_length=50)):
    r"""
    更新部门的信息，以传入的路径参数name唯一指定(若不指定则更新所有部门)
    可选修改name和remark
    """
    return dept_service.update_dept(name, dept)
