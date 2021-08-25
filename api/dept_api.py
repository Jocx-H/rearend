#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Query, HTTPException
from model.dept import Department
from model.code import Code400
from service import dept_service
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
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
    try:
        result = dept_service.add_dept(dept)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.delete("/remove", responses={400: {"model": Code400}})
async def remove_dept(name: str = Query(..., min_length=1, max_length=50)):
    r"""
    删除部门，以查询参数name唯一指定
    """
    try:
        result = dept_service.remove_dept(name)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.get("/get", responses={400: {"model": Code400}})
async def get_dept(name: str = Query(..., min_length=1, max_length=50)):
    r"""
    获取部门的信息，以查询参数name唯一指定
    """
    try:
        result = dept_service.get_dept(name)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.put("/update", responses={400: {"model": Code400}})
async def update_dept(dept: Department):
    r"""
    更新部门的信息，以传入的name唯一指定，可选修改name和remark
    """
    try:
        result = dept_service.update_dept(dept)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)
