#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.code import Code400
from service import face_recognition_service
from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
import traceback
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from service import login_service

# 构建api路由
router = APIRouter(
    prefix="/login",
    tags=["Login"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/passwd")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    r"""
    网络登录验证的api
    """
    res = login_service.login_check(form_data.username, form_data.password)
    if res is login_service.NOONE:
        raise HTTPException(status_code=400, detail="查无此人")
    elif res is login_service.PASSWORDWRONG:
        raise HTTPException(status_code=400, detail="密码错误")
    return {'code': 200, 'message': 'success'}



@router.post("/face", responses={400: {"model": Code400}})
async def face_read(file: UploadFile = File(...)):
    try:
        content = await file.read()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端语法错误")
    res = face_recognition_service.face_reco_service(content)

    if res:
        return {'code': 200, 'message': 'success'}
    raise HTTPException(status_code=400, detail="人脸未能识别")
