#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Query, Path, File, UploadFile, Form
from model.document import Document
from model.code import Code400
from service import document_service
from typing import Optional, List
import asyncio

# 构建api路由
router = APIRouter(
    prefix="/document",
    tags=["Document"],
)


@router.post("/add", responses={400: {"model": Code400}})
async def add_document(title: str = Form(...),
                       username: str = Form(...),
                       files: List[UploadFile] = File(None),
                       remark: Optional[str] = Form(None, max_length=300)):
    r"""
    创建document的同时上传文件，支持同一文档(title)多文件上传
    若document已存在，也可以用于添加文件
    title, username 必选，remark可选
    可以不上传文件，但是也不能传一个空值过来，即文档中Send empty value
    """
    return await document_service.add_document(
        files, title, username, remark)


@router.delete("/remove-all", responses={400: {"model": Code400}})
async def remove_all_documents():
    r"""
    删除全部文档
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, document_service.remove_document, None)


@router.delete("/remove/{title}", responses={400: {"model": Code400}})
async def remove_document(title: str = Path(..., min_length=1, max_length=50),
                          filename: str = Query(None, min_length=1)):
    r"""
    删除指定title（路径参数）的document中的
    特定文件filename（查询参数，注意包括文件名后缀名）
    若不指定文件则删除整个文档
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, document_service.remove_document, title, filename)


@router.get("/get-all", responses={400: {"model": Code400}})
async def get_all_documents(limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取全部文件的信息
    可以选择limit和skip
    返回的链接是不带公网IP的
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, document_service.get_document, None, limit, skip)


@router.get("/get/{title}", responses={400: {"model": Code400}})
async def get_document(title: str = Path(..., min_length=1, max_length=50),
                       limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取文件的信息，以路径参数title唯一指定
    可以选择limit和skip
    返回的链接是不带公网IP的
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, document_service.get_document, title, limit, skip)


@router.put("/update/{title}", responses={400: {"model": Code400}})
async def update_document(document: Document,
                          title: str = Path(..., min_length=1, max_length=50)):
    r"""
    更新文件的信息，以传入的title唯一指定
    可选修改username, remark, title, create_time(要按照timestamp格式，不建议修改)
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, document_service.update_document, title, document)
