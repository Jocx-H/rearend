#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from service import login_service

# 构建api路由
router = APIRouter(
    prefix="/login",
    tags=["login"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    r"""
    网络登录验证的api
    """
    res = login_service.login_check(form_data.username, form_data.password)
    if res is login_service.NOONE:
        raise HTTPException(status_code=400, detail="查无此人")
    elif res is login_service.PASSWORDWRONG:
        raise HTTPException(status_code=400, detail="密码错误")
    return {'code': 200, 'massage': 'success'}