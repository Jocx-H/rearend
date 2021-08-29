#!/usr/bin/env python
# -*- coding: utf-8 -*-
from json import JSONDecoder
from fastapi import UploadFile
from requests import post as face_post
from dao import crud
from typing import Optional, BinaryIO, Union
from typing import BinaryIO, Union
from fastapi import UploadFile
from json import JSONDecoder
from hashlib import md5
from dao import crud
from fastapi import HTTPException
import os
import traceback

FACE_PATH = "assets/private/face_img"
TEMP_PATH = "assets/private/tmp"
THRESHOLD = 70  # 人脸识别通过的阈值

SECRET_KEY = {
    "key": "iXWmKDAuviqmnDx9KcGcb5f26VXD8qro",
    "secret": "aDChdAEjL4hY5AYfshQL1rW4DhUVzyWu"
}  # 密钥


async def face_add(file: UploadFile, username: str):
    r"""
    注册人脸
    """
    content = await file.read()
    # 先把数据流存成图片再检测
    suffix = '.' + file.filename.split('.')[-1]
    assert suffix == '.jpg' or suffix == '.png', "只支持JPG(JPEG)，PNG"
    assert type(content) is bytes, "文件流应该是Bytes类型吧？"+str(content)
    # 先存到临时的文件待检测
    fake_path = os.path.join(TEMP_PATH, username+'_tmp'+suffix)
    with open(fake_path, 'wb') as f:
        f.write(content)
    res = detect_face(fake_path)
    if res:  # 如果是人脸就保存图片
        os.remove(fake_path)
        face_path = os.path.join(FACE_PATH, username+suffix)
        with open(face_path, 'wb') as f:
            f.write(content)
    else:
        os.remove(fake_path)
        raise HTTPException(status_code=400, detail="所上传图片中检测不到人脸！")
    return {'code': 200, 'message': 'success'}

def detect_face(img_path: str) -> bool:
    r"""
    检测注册的图片是否是人脸
    """
    face_api_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"

    data = {"api_key": SECRET_KEY['key'],
            "api_secret": SECRET_KEY['secret']}
    
    try:
        with open(img_path, 'rb') as f:
            response = face_post(face_api_url, data=data, files={"image_file": f})
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        # 如果不是人脸则`req_dict[face]`是None
        if req_dict['faces'] is None or len(req_dict['faces']) == 0:
            return False
        return True
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        return False


def compare_face(file_buffer_1: BinaryIO, file_buffer_2: BinaryIO):
    r"""
    比较人脸
    """
    face_api_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"

    data = {"api_key": SECRET_KEY['key'],
            "api_secret": SECRET_KEY['secret']}

    files = {"image_file1": file_buffer_1, "image_file2": file_buffer_2}

    response = face_post(face_api_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    if 'confidence' in req_dict.keys():
        return req_dict['confidence']
    else:
        return None


async def face_recognition(file: UploadFile):
    r"""
    人脸登录，用于比较人脸信息
    file，传进来的照片文件
    """
    # 处理传进来的照片
    suffix = '.'+file.filename.split('.')[-1]
    assert suffix == '.jpg' or suffix == '.png', "只支持JPG(JPEG)，PNG"
    content = await file.read()
    assert type(content) is bytes, "文件流应该是Bytes类型吧？"+str(content)
    with open(os.path.join(TEMP_PATH, 'temp'+suffix), 'wb') as f:
        f.write(content)

    # 处理已存图片
    for img_file in os.listdir(FACE_PATH):
        with open(os.path.join(FACE_PATH, img_file), "rb") as compared_img:
            with open(os.path.join(TEMP_PATH, 'temp'+suffix), 'rb') as img:
                res = compare_face(compared_img, img)
                if res is not None and res >= THRESHOLD:
                    username = img_file.split('.')[0]
                    infos = ['username', 'status', 'name', 'sex',
                             'card_id', 'avatar_url', 'department', 'job',
                             'address', 'post_code', 'tel', 'phone',
                             'qq_num', 'email', 'party', 'birthday', 'nationality',
                             'education', 'speciality', 'hobby', 'remark', 'create_time']
                    user_check = crud.select_items('user_inf',
                                                   infos,
                                                   where={'username': username})
                    if len(user_check) > 0:
                        user_check[0]['has_face'] = 1
                        return user_check[0]
    raise HTTPException(status_code=400, detail="未匹配到人脸信息")


def hash_password(password: str):
    r"""
    hd5加密密码
    """
    user_hash = md5()
    user_hash.update(password.encode(encoding='utf-8'))
    return user_hash.hexdigest()


def login_check(username, password):
    r"""
    检查密码是否与数据库中密码相符
    """
    infos = ['username', 'password', 'status', 'name', 'sex',
             'card_id', 'avatar_url', 'department', 'job',
             'address', 'post_code', 'tel', 'phone',
             'qq_num', 'email', 'party', 'birthday', 'nationality',
             'education', 'speciality', 'hobby', 'remark', 'create_time']
    user_check = crud.select_items('user_inf',
                                   infos,
                                   where={'username': username})
    if len(user_check) == 0:
        raise HTTPException(status_code=400, detail="查无此人")
    else:
        user_check = user_check[0]
        if user_check['password'] != hash_password(password):
            raise HTTPException(status_code=400, detail="密码错误")
    del user_check['password']
    user_check['has_face'] = has_face(username)
    return user_check


def has_face(username: str):
    if os.path.exists(os.path.join(FACE_PATH, username+'.jpg')) or \
    os.path.exists(os.path.join(FACE_PATH, username+'.png')):
        return 1
    else:
        return 0
