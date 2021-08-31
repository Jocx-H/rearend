#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.notice import Notice
from dao import crud
from typing import Optional
from api.utils import exception_handler


@exception_handler
def add_notice(title: str,
               username: str,
               content: Optional[str]):
    r"""
    添加公告，title, username必选, content可选
    """
    columns = ['title', 'username']
    values = [title, username]
    if content is not None:
        columns.append('content')
        values.append(content)
    crud.insert_items("notice_inf", columns=columns, values=[values])
    return crud.select_items("notice_inf", columns=['create_time'],
                             where={'title': title})[0]


@exception_handler
def remove_notice(title: Optional[str]):
    r"""
    删除公告，以路径参数title唯一指定
    """   
    if title is None:
        return crud.delete_items('notice_inf', where=None)
    else:
        return crud.delete_items('notice_inf', where={'title': title})


@exception_handler
def get_notice(title: Optional[str], limit: Optional[int], skip: int):
    r"""
    获取公告的信息，以路径参数title唯一指定
    """
    if title is None:
        return crud.select_items('notice_inf',
                                 columns=['username', 'content',
                                          'title', 'create_time'],
                                 where=None, limit=limit, skip=skip)
    else:
        return crud.select_items('notice_inf', 
        columns=['username', 'content', 'title', 'create_time'],
        where={'title': title}, limit=limit, skip=skip)


@exception_handler
def update_notice(title: Optional[str], notice: Notice):
    r"""
    更新公告的信息，以传入的title唯一指定
    可选修改username, content, title, create_time(要按照timestamp格式，不建议修改)
    """
    items = notice.dict(exclude_unset=True)
    if title is None:
        return crud.update_items('notice_inf', items, where=None)
    else:
        return crud.update_items('notice_inf', items, where={'title':title})
