#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model import document
from model.document import Document
from dao import crud
from typing import Optional, List
from fastapi import UploadFile
import os
import time
import shutil

DOCUMENT_PATH = 'assets/public/document'

async def add_document(document: Document,
                 files: List[UploadFile]):
    r"""
    上传文件，支持同一文档(title)多文件上传
    title, username 必选，remark可选
    """
    document_dict = document.dict()
    columns = []
    values = []
    for k in document_dict.keys():
        if document_dict[k] != None:
            columns.append(k)
            values.append(document_dict[k])
    folder = os.path.join(DOCUMENT_PATH, document_dict['title'])
    if not os.path.exists(folder):
        os.mkdir(folder) # 每个document用一个文件夹存文件
    start = time.time()
    for file in files:
        content = await file.read()
        with open(os.path.join(folder, file.filename), 'wb') as f:
            f.write(content)
    msg = crud.insert_items("document_inf", columns=columns, values=[values])
    return {"message": msg, 'time': time.time() - start, 'filename': [file.filename for file in files]}



def remove_document(title: Optional[str]):
    r"""
    删除文档及其目录下的所有文件，以路径参数title唯一指定
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
        if os.path.exists(os.path.join(DOCUMENT_PATH, title)):
            shutil.rmtree(os.path.join(DOCUMENT_PATH, title))
        return crud.delete_items('document_inf', where={'title': title})


def get_document(title: Optional[str], limit: Optional[int], skip: int):
    r"""
    获取文档的信息，以路径参数title唯一指定
    """
    if title is None:
        result = crud.select_items('document_inf',
                                 columns=['username', 'remark', 'filename',
                                          'title', 'create_time'],
                                 where=None, limit=limit, skip=skip)
    else:
        result =  crud.select_items('document_inf', 
        columns=['username', 'remark', 'filename', 'title', 'create_time'],
        where={'title': title}, limit=limit, skip=skip)
    for r in result:  # 添加文件下载地址
        r['file_urls'] = [filename for filename in os.listdir(os.path.join(DOCUMENT_PATH, r['title']))]
    return result


# def update_document(title: Optional[str], document: Document):
#     r"""
#     更新文档的信息，以传入的title唯一指定
#     可选修改username, remark, title, filename, create_time(要按照timestamp格式，不建议修改)
#     """
#     items = document.dict(exclude_unset=True)
#     if title is None:
#         return crud.update_items('document_inf', items, where=None)
#     else:
#         return crud.update_items('document_inf', items, where={'title':title})
