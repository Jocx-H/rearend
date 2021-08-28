#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from fastapi import APIRouter, Query, HTTPException, Path, File, UploadFile
from model.user import User
from model.code import Code400
from service import user_service, face_recognition_service
from fastapi.encoders import jsonable_encoder
from typing import Optional

# 构建api路由
router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/add_user", responses={400: {"model": Code400}})
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
        "race": "黄种人",
        "education": "高中",
        "speciality": "无",
        "hobby": "看剧",
        "remark": "我是李新浩"
    }
    """
    try:
        assert user.username is not None, "必须传入username"
        if user.password is None:
            user.password = "123456"
        result = user_service.add_user(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)


@router.post("/change-avatar/{username}", responses={400: {"model": Code400}})
async def change_avatar(file: UploadFile = File(...),
                        username: str = Path(..., min_length=1, max_length=20)):
    r"""
    修改用户的头像，以路径参数username指定用户
    """
    try:
        result = await user_service.change_avatar(file, username)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)


@router.delete("/remove/{username}", responses={400: {"model": Code400}})
async def remove_user(username: str = Path(..., min_length=1, max_length=20)):
    r"""
    删除员工，以路径参数username唯一指定
    """
    try:
        result = user_service.remove_user(username)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)


@router.get("/get-all", responses={400: {"model": Code400}})
async def get_all_users(limit: Optional[int] = Query(10),
                        skip: int = Query(0)):
    r"""
    获取全体员工的信息
    可以选择limit和skip。limit默认是10，skip默认是0
    """
    try:
        result = user_service.get_user(None, limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)


@router.get("/search/{name}", responses={400: {"model": Code400}})
async def search_user(name: str = Path(..., min_length=1, max_length=20)):
    r"""
    根据username或name搜索指定员工
    """
    try:
        result1 = user_service.get_user(
            where={'name': name}, limit=None, skip=0)
        result2 = user_service.get_user(
            where={'username': name}, limit=None, skip=0)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result1+result2)


@router.post("/get", responses={400: {"model": Code400}})
async def get_user(where: User = None,
                   limit: Optional[int] = Query(None),
                   skip: int = Query(0)):
    r"""
    获取指定条件(where)的员工信息
    可以选择limit和skip。limit默认是20，skip默认是0
    """
    try:
        if where is not None:
            result = user_service.get_user(where.dict(), limit, skip)
        else:
            result = user_service.get_user(None, limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)


@router.put("/update/{username}", responses={400: {"model": Code400}})
async def update_user(user: User,
                      username: str = Path(..., min_length=1, max_length=20)):
    r"""
    更新员工信息，以路径参数username唯一指定
    """
    try:
        result = user_service.update_user(username, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)


@router.post("/face-register", responses={400: {"model": Code400}})
async def face_register(username: str, file: UploadFile = File(...)):
    try:
        content = await file.read()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    res = face_recognition_service.face_add(content, username)  # 读入图像二进制流

    if res:
        return {'code': 200, 'message': 'success'}
    raise HTTPException(status_code=400, detail="不是人脸")
