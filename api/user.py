#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 引入路由管理
from fastapi import APIRouter
# 让数据以json的格式返回
from fastapi.responses import JSONResponse
from service import user_service

# 构建api路由
router = APIRouter()




@router.get("/getUsers", tags=["用户"])
async def get_users(uname: str):
    r"""
    获取用户的信息数据
    """
    print(uname)
    # 1.通过调用相应的服务得到对应的反馈
    return user_service.get_user_infos(uname)
