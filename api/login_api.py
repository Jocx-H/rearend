#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.code import Code400
from fastapi import Depends, APIRouter, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from service import login_service
import asyncio

# 构建api路由
router = APIRouter(
    prefix="/login",
    tags=["Login"],
)



@router.post("/passwd")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    r"""
    网络登录验证的api，返回data和token，
    其中data中has_face=1表示人脸已经注册，0为未注册
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, login_service.login_check,
                                        form_data.username, form_data.password)
    return result


@router.post("/face-recognition", responses={400: {"model": Code400}})
async def face_recognition(file: UploadFile = File(...)):
    r"""
    人脸登录验证的api，返回data和token
    """
    result = await login_service.face_recognition(file)
    return {'code': 200, 'message': 'success', 'data': result}


@router.post("/face-register", responses={400: {"model": Code400}})
async def face_register(username: str, file: UploadFile = File(...)):
    r"""
    注册人脸信息
    以username指定，若上传图片中识别不到人脸则注册失败
    """
    return await login_service.face_add(file, username)  # 读入图像二进制流
