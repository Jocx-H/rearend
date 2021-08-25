#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5
from dao import crud

NOONE = 0
PASSWORDWRONG = 1
SUCCESS = 2


def hash_password(password: str):
    r"""
    哈希一下密码。目前用假的hash代替
    """
    user_hash = md5()
    user_hash.update(password.encode(encoding='utf-8'))
    return user_hash.hexdigest()


def login_check(name, password):
    r"""
    利用检查用户的名字
    """
    user_check = crud.select_items('user_inf',
                                   ['username', 'password'],
                                   where={'username': name})
    if len(user_check) is 0:
        return NOONE
    else:
        user_check = user_check[0]
        if user_check['password'] != hash_password(password):
            return PASSWORDWRONG
    return SUCCESS