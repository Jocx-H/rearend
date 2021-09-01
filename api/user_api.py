#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Query, Depends, Path, File, UploadFile
from model.user import User
from model.code import Code400
from service import user_service
from typing import Optional
import asyncio
from api.utils import check_current_admin_user, check_current_user

# 构建api路由
router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/add_user", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_admin_user)])
async def add_user(user: User):
    r"""
    添加员工，员工的username必填
    password默认为123456, 默认权限为普通用户
    不需要填create_time
    Example:
    {
        "username": "20185525",
        "password": "010099",
        "status": 1,
        "name": "李新浩",
        "sex": 1,
        "card_id": "36073020001001xxxx",
        "department": "技术部",
        "phone": "18470435117",
        "tel":"xxxxxx",
        "address":"大house",
        "postcode":"100000",
        "qq_num": "1520491933",
        "email": "1520491933@qq.com",
        "party": "预备党员",
        "birthday": "2017-03-02",
        "nationality": "中国大陆",
        "education": "高中",
        "speciality": "无",
        "hobby": "看剧",
        "remark": "我是李新浩"
    }
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, user_service.add_user, user)
    

@router.post("/change-avatar/{username}", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_user)])
async def change_avatar(file: UploadFile = File(...),
                        username: str = Path(..., min_length=1, max_length=20)):
    r"""
    修改用户的头像，以路径参数username指定用户
    """
    return await user_service.change_avatar(file, username)
    

@router.delete("/remove/{username}", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_admin_user)])
async def remove_user(username: str = Path(..., min_length=1, max_length=20)):
    r"""
    删除员工，以路径参数username唯一指定
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, user_service.remove_user, username)
    

@router.get("/get-all", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_user)])
async def get_all_users(limit: Optional[int] = Query(10),
                        skip: int = Query(0)):
    r"""
    获取全体员工的信息
    可以选择limit和skip。limit默认是10，skip默认是0
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, user_service.get_user, None, limit, skip)


@router.get("/search/{name}", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_user)])
async def search_user(name: str = Path(..., min_length=1, max_length=20)):
    r"""
    根据username或name搜索指定员工
    """
    loop = asyncio.get_event_loop()
    result1 = await loop.run_in_executor(None, user_service.get_user,
        {'name': name}, None, 0)
    result2 = await loop.run_in_executor(None, user_service.get_user,
        {'username': name}, None, 0)
    return result1+result2


@router.post("/get", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_user)])
async def get_user(where: User = None,
                   limit: Optional[int] = Query(None),
                   skip: int = Query(0)):
    r"""
    获取指定条件(where)的员工信息
    可以选择limit和skip。limit默认是20，skip默认是0
    """
    loop = asyncio.get_event_loop()
    if where is None:
        return await loop.run_in_executor(None, user_service.get_user, None, limit, skip)
    else:
        return await loop.run_in_executor(None, user_service.get_user, where.dict(), limit, skip)


@router.put("/update/{username}", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_user)])
async def update_user(user: User,
                      username: str = Path(..., min_length=1, max_length=20)):
    r"""
    更新员工信息，以路径参数username唯一指定
    赋予了非管理员账号修改用户的权力（这里由于接口未区分开存在潜在的漏洞）
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, user_service.update_user, username, user)
    




