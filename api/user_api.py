#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 引入路由管理
from fastapi import APIRouter, Query, HTTPException
from model.code import Code400
from model.user import User
from service import user_service
from fastapi.encoders import jsonable_encoder
# 构建api路由
router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/add", responses={400: {"model": Code400}})
async def add_dept(user: User):
    r"""
    添加用户，name必选，remark可选
    """
    try:
        result = user_service.add_user(user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.delete("/remove", responses={400: {"model": Code400}})
async def remove_dept(name: str = Query(..., min_length=1, max_length=50)):
    r"""
    删除用户，以查询参数name唯一指定
    """
    try:
        result = user_service.remove_dept(name)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.get("/get", responses={400: {"model": Code400}})
async def get_dept(name: str = Query(..., min_length=1, max_length=50)):
    r"""
    获取用户的信息，以查询参数name唯一指定
    """
    try:
        result = user_service.get_dept(name)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.put("/update", responses={400: {"model": Code400}})
async def update_dept(user: User):
    r"""
    更新用户的信息，以传入的name唯一指定，可选修改name和remark
    """
    try:
        result = user_service.update_dept(user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


