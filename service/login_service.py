#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5
from dao import crud

NOONE = 0
PASSWORDWRONG = 1
SUCCESS = 2


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
    user_check = crud.select_items('user_inf',
                                    ['password'],
                                   where={'username': username})
    if len(user_check) == 0:
        return NOONE
    else:
        user_check = user_check[0]
        if user_check['password'] != hash_password(password):
            return PASSWORDWRONG
    return SUCCESS