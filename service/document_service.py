#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.document import Document
from dao import crud
from typing import Optional, List
from fastapi import UploadFile, HTTPException
import os
import time
import shutil

DOCUMENT_PATH = 'assets/public/document'
DOCUMENT_URL = 'resources/document'


async def add_document(files: List[UploadFile],
                       title: str,
                       username: str,
                       remark: Optional[str]):
    r"""
    创建document的同时上传文件，支持同一文档(title)多文件上传
    若document已存在，也可以用于添加文件
    title, username 必选，remark可选
    """
    columns = ['title', 'username']
    values = [title, username]
    if remark is not None:
        columns.append('remark')
        values.append(remark)
    folder = os.path.join(DOCUMENT_PATH, title)
    if not os.path.exists(folder):
        os.mkdir(folder)  # 每个document用一个文件夹存文件
        crud.insert_items(
            "document_inf", columns=columns, values=[values])
    start = time.time()
    for file in files:
        content = await file.read()
        with open(os.path.join(folder, file.filename), 'wb') as f:
            f.write(content)
    return {"message": "success", 'time': time.time() - start,
            'filename': [file.filename for file in files]}


def remove_document(title: Optional[str], filename: Optional[str]) -> str:
    r"""
    删除指定title（路径参数）的document中的特定文件filename（查询参数）
    若不指定文件则删除整个文档
    """
    if title is None:
        # 删除document目录下所有文件和文件夹
        for f in os.listdir('assets/public/document'):
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)
        return crud.delete_items('document_inf', where=None)
    else:
        if filename is None:
            if os.path.exists(os.path.join(DOCUMENT_PATH, title)):
                shutil.rmtree(os.path.join(DOCUMENT_PATH, title))
                return crud.delete_items('document_inf', where={'title': title})
        else:
            if os.path.exists(os.path.join(DOCUMENT_PATH, title, filename)):
                os.remove(os.path.join(DOCUMENT_PATH, title, filename))
            else:
                raise HTTPException(
                    status_code=400, detail="该文件不存在，请确认文件名(包括后缀)无误")
        return "success"


def get_document(title: Optional[str], limit: Optional[int], skip: int):
    r"""
    获取文档的信息，以路径参数title唯一指定
    """
    if title is None:
        result = crud.select_items('document_inf',
                                   columns=['username', 'remark',
                                            'title', 'create_time'],
                                   where=None, limit=limit, skip=skip)
    else:
        result = crud.select_items('document_inf',
                                   columns=['username', 'remark',
                                            'title', 'create_time'],
                                   where={'title': title}, limit=limit, skip=skip)
    for r in result:  # 添加文件下载地址
        r['file_urls'] = [os.path.join(DOCUMENT_URL, r['title'], filename) for filename in os.listdir(
            os.path.join(DOCUMENT_PATH, r['title']))]
        r['filenames'] = [filename for filename in os.listdir(
            os.path.join(DOCUMENT_PATH, r['title']))]
    return result


def update_document(title: str, document: Document):
    r"""
    更新文件的信息，以传入的title唯一指定
    可选修改username, remark, title, create_time(要按照timestamp格式，不建议修改)
    """
    items = document.dict(exclude_unset=True)
    if 'title' in items.keys():  # 文件夹更名
        os.rename(os.path.join(DOCUMENT_PATH, title),
                  os.path.join(DOCUMENT_PATH, items['title']))
    return crud.update_items('document_inf', items, where={'title': title})
