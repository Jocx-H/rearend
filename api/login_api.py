#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

# 构建api路由
router = APIRouter(
    prefix="/login",
    tags=["login"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/{token}")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


# @router.get("/{token}")
# async def read_me(token: str):
#     return {"hello": "world"}