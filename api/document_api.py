#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Query, HTTPException, Body, Path
from model.document import Document
from model.code import Code400
from service import document_service
from fastapi.encoders import jsonable_encoder
from typing import Optional
from pydantic import BaseModel, Field

# 构建api路由
router = APIRouter(
    prefix="/document",
    tags=["Document"],
)


@router.post("/add", responses={400: {"model": Code400}})
async def add_document(title: str = Body(..., min_length=1, max_length=50),
                     username: str = Body(..., min_length=1, max_length=20,
                     description="The username of notifier"),
                     filename: str = Body(None, min_length=1, max_length=300),
                     remark: Optional[str] = Body(None, max_length=300)):
    r"""
    添加文件，title, username,filename必选，remark可选
    """
    try:
        result = document_service.add_document(title, username, filename,remark)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.delete("/remove-all", responses={400: {"model": Code400}})
async def remove_all_documents():
    r"""
    删除全部文件
    """
    try:
        result = document_service.remove_document(None)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)

@router.delete("/remove/{title}", responses={400: {"model": Code400}})
async def remove_document(title: str = Path(..., min_length=1, max_length=50)):
    r"""
    删除文件，以路径参数title唯一指定
    """
    try:
        result = document_service.remove_document(title)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.get("/get-all", responses={400: {"model": Code400}})
async def get_all_documents(limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取全部文件的信息
    可以选择limit和skip
    """
    try:
        result = document_service.get_document(None, limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)

@router.get("/get/{title}", responses={400: {"model": Code400}})
async def get_document(title: str = Path(..., min_length=1, max_length=50),
                     limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取文件的信息，以路径参数title唯一指定
    可以选择limit和skip
    """
    try:
        result = document_service.get_document(title, limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)


@router.put("/update-all", responses={400: {"model": Code400}})
async def update_all_documents(document: Document):
    r"""
    更新全部文件的信息
    可选修改username, remark, title,filename create_time(要按照timestamp格式，不建议修改)
    """
    try:
        result = document_service.update_document(None, document)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)

@router.put("/update/{title}", responses={400: {"model": Code400}})
async def update_document(document: Document,
                        title: str = Path(..., min_length=1, max_length=50)):
    r"""
    更新文件的信息，以传入的title唯一指定
    可选修改username, remark, title,filename create_time(要按照timestamp格式，不建议修改)
    """
    try:
        result = document_service.update_document(title, document)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    return jsonable_encoder(result)
