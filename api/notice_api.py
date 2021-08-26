#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from fastapi import APIRouter, Query, HTTPException, Body, Path
from model.notice import Notice
from model.code import Code400
from service import notice_service
from fastapi.encoders import jsonable_encoder
from typing import Optional

# 构建api路由
router = APIRouter(
    prefix="/notice",
    tags=["Notice"],
)


@router.post("/add", responses={400: {"model": Code400}})
async def add_notice(title: str = Body(..., min_length=1, max_length=50),
                     username: str = Body(..., min_length=1, max_length=20,
                     description="The username of notifier"),
                     content: Optional[str] = Body(None, max_length=300)):
    r"""
    添加公告，title, username必选，content可选
    """
    try:
        result = notice_service.add_notice(title, username, content)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.delete("/remove-all", responses={400: {"model": Code400}})
async def remove_all_notices():
    r"""
    删除全部公告
    """
    try:
        result = notice_service.remove_notice(None)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.delete("/remove/{title}", responses={400: {"model": Code400}})
async def remove_notice(title: str = Path(..., min_length=1, max_length=50)):
    r"""
    删除公告，以路径参数title唯一指定
    """
    try:
        result = notice_service.remove_notice(title)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.get("/get-all", responses={400: {"model": Code400}})
async def get_all_notices(limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取全部公告的信息
    可以选择limit和skip
    """
    try:
        result = notice_service.get_notice(None, limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.get("/get/{title}", responses={400: {"model": Code400}})
async def get_notice(title: str = Path(..., min_length=1, max_length=50),
                     limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取公告的信息，以路径参数title唯一指定
    可以选择limit和skip
    """
    try:
        result = notice_service.get_notice(title, limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.put("/update-all", responses={400: {"model": Code400}})
async def update_all_notices(notice: Notice):
    r"""
    更新全部公告的信息
    可选修改username, content, title, create_time(要按照timestamp格式，不建议修改)
    """
    try:
        result = notice_service.update_notice(None, notice)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.put("/update/{title}", responses={400: {"model": Code400}})
async def update_notice(notice: Notice,
                        title: str = Path(..., min_length=1, max_length=50)):
    r"""
    更新公告的信息，以传入的title唯一指定
    可选修改username, content, title, create_time(要按照timestamp格式，不建议修改)
    """
    try:
        result = notice_service.update_notice(title, notice)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)
