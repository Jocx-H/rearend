#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Query, HTTPException
from model.user import User
from model.code import Code400
from service import user_service
from fastapi.encoders import jsonable_encoder
from typing import Optional, Dict, Union

# 构建api路由
router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/add_user", responses={400: {"model": Code400}})
async def add_dept(user: User):
    r"""
    添加员工，员工的username，password必填
    """
    try:
        assert user.username is not None \
               and user.password is not None, "必须传入username或者password"
        result = user_service.add_user(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.delete("/remove/{username}", responses={400: {"model": Code400}})
async def remove_user(username: str):
    r"""
    只能通过主键id来删除员工
    """
    try:
        result = user_service.remove_user(username)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.post("/get/{username}", responses={400: {"model": Code400}})
async def get_dept(username: Optional[str] = None,
                   where: Optional[Dict[str, Union[str, int, float]]] = None,
                   limit: Optional[int] = Query(20),
                   skip: int = Query(0)):
    r"""
    获取员工信息的装置
    可以选择limit和skip。limit默认是20，skip默认是0
    """
    try:
        result = user_service.get_user(username, where, limit, skip)
        if result is user_service.WRONG:
            raise HTTPException(status_code=400, detail="查无此人")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.put("/update/{username}", responses={400: {"model": Code400}})
async def update_dept(user: User,
                      username: str):
    r"""
    更新员工信息，以user_id为唯一识别
    """
    try:
        result = user_service.update_user(username, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)