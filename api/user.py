#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 引入路由管理
from fastapi import APIRouter
# 让数据以json的格式返回
from fastapi.responses import JSONResponse
from service import user_service

# 构建api路由
router = APIRouter()


# @router.get("/getUsers", tags=["用户"])
# async def get_users(uname: str):
#     r"""
#     获取用户的信息数据
#     """
#     print(uname)
#     # 1.通过调用相应的服务得到对应的反馈
#     return user_service.get_user_infos(uname)


# 通过路径参数传递表单名字
# 通过查询参数传递服务类型
@router.get("/user/{d_name}")
async def get_data(
        d_name: str, skip: int = 0, limit: int = 20
    ):
    return user_service.get_data(
        d_name, skip=skip, limit=limit
    )


# 通过路径参数传递表单名字
# 通过查询参数传递服务类型
@router.get("/user/{d_name}")
async def delete_data(
        d_name: str, key: str = None, where: str = None
    ):
    return user_service.delete_data(
        d_name, key=key, where=where
    )