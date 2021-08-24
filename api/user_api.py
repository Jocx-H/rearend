#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 引入路由管理
from fastapi import APIRouter
from service import user_service

# 构建api路由
router = APIRouter(
    prefix="/user",
    tags=["User"],
)


# @router.get("/getUsers")
# async def get_users(uname: str):
#     r"""
#     获取用户的信息数据
#     """
#     print(uname)
#     # 1.通过调用相应的服务得到对应的反馈
#     return user_service.get_user_infos(uname)


