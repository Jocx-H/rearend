#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.code import Code400
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
    网络登录验证的api，返回has_face=1表示人脸已经注册，0为未注册
    """
    try:
        result = login_service.login_check(form_data.username, form_data.password)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return {'code': 200, 'message': 'success', 'data': result}


@router.post("/face-recognition", responses={400: {"model": Code400}})
async def face_recognition(file: UploadFile = File(...)):
    try:
        result = await login_service.face_recognition(file)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return {'code': 200, 'message': 'success', 'data': result}


@router.post("/face-register", responses={400: {"model": Code400}})
async def face_register(username: str, file: UploadFile = File(...)):
    r"""
    注册人脸信息
    以username指定，若上传图片中识别不到人脸则注册失败
    """
    try:
        result = await login_service.face_add(file, username)  # 读入图像二进制流
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return result


# @router.get("/has-face/{username}", responses={400: {"model": Code400}})
# async def has_face(username: str):
#     r"""
#     判断指定username用户是否注册人脸信息
#     """
#     try:
#         result = login_service.has_face(username)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         print(e)
#         traceback.print_exc()
#         raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
#     return result




