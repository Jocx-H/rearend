#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from service import face_recognition_service
from model.code import Code400

# 构建api路由
router = APIRouter(
    prefix="/login",
    tags=["Login"],
)


@router.post("/face", responses={400: {"model": Code400}})
async def face_read(file: UploadFile = File(...)):
    try:
        content = await file.read()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="客户端语法错误")
    res = face_recognition_service.face_reco_service(content)

    if res:
        return {'code': 200, 'message': 'success'}
    raise HTTPException(status_code=400, detail="人脸未能识别")