#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model import document
from model.document import Document
from dao import crud
from typing import Optional


def add_document(title: str,
               username: str,
               filename: str,
               remark: Optional[str]):
    r"""
    上传文档，title, username, filename必选,remark可选
    """
    columns = ['title', 'username', 'filename', 'remark']
    values = [title, username, filename, remark]
    crud.insert_items("document_inf", columns=columns, values=[values])
    return crud.select_items("document_inf", columns=['create_time'],
                             where={'title': title})[0]


def remove_document(title: Optional[str]):
    r"""
    删除文档，以路径参数title唯一指定
    """
    if title is None:
        return crud.delete_items('document_inf', where=None)
    else:
        return crud.delete_items('document_inf', where={'title': title})


def get_document(title: Optional[str], limit: Optional[int], skip: int):
    r"""
    获取文档的信息，以路径参数title唯一指定
    """
    if title is None:
        return crud.select_items('document_inf',
                                 columns=['username', 'remark', 'filename'
                                          'title', 'create_time'],
                                 where=None)
    else:
        return crud.select_items('document_inf', 
        columns=['username', 'remark', 'filename', 'title', 'create_time'],
        where={'title': title}, limit=limit, skip=skip)


def update_document(title: Optional[str], document: Document):
    r"""
    更新文档的信息，以传入的title唯一指定
    可选修改username, remark, title, filename, create_time(要按照timestamp格式，不建议修改)
    """
    items = document.dict(exclude_unset=True)
    if title is None:
        return crud.update_items('document_inf', items, where=None)
    else:
        return crud.update_items('document_inf', items, where={'title':title})