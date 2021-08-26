#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5
from dao import crud
from fastapi import HTTPException



def hash_password(password: str):
    r"""
    hd5加密密码
    """
    user_hash = md5()
    user_hash.update(password.encode(encoding='utf-8'))
    return user_hash.hexdigest()


def login_check(username, password):
    r"""
    检查密码是否与数据库中密码相符
    """
    infos = ['username', 'password', 'status', 'name', 'sex',
             'card_id', 'avatar_url', 'department', 'job',
             'address', 'post_code', 'tel', 'phone',
             'qq_num', 'email', 'party', 'birthday', 'race',
             'education', 'speciality', 'hobby', 'remark', 'create_time']
    user_check = crud.select_items('user_inf',
                                    infos,
                                   where={'username': username})
    if len(user_check) == 0:
        raise HTTPException(status_code=400, detail="查无此人")
    else:
        user_check = user_check[0]
        if user_check['password'] != hash_password(password):
            raise HTTPException(status_code=400, detail="密码错误")
    del user_check['password']
    return user_check
