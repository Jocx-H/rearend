#!/usr/bin/env python
# -*- coding: utf-8 -*-
from json import JSONDecoder
from fastapi import UploadFile
from requests import post as face_post
from dao import crud
from typing import Optional, BinaryIO, BinaryIO
from fastapi import UploadFile, status
from json import JSONDecoder
from hashlib import md5
from dao import crud
from fastapi import HTTPException
import os
import traceback
from api.utils import exception_handler, async_exception_handler, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from datetime import datetime, timedelta
from jose import jwt
import json

# 读取本地安全配置
with open("config.json") as f:
    db_configs = json.load(f)['safe']

FACE_PATH = db_configs['face_path']
TEMP_PATH = db_configs['temp_path']
THRESHOLD = db_configs['face_threshold']
FACE_SECRET_KEY = db_configs['face_secret_key']

# 人脸注册部分
@async_exception_handler
async def face_add(file: UploadFile, username: str):
    r"""
    注册人脸
    """
    content = await file.read()
    # 先把数据流存成图片再检测
    suffix = '.' + file.filename.split('.')[-1]
    assert suffix == '.jpg' or suffix == '.jpeg' or suffix == '.png', "只支持JPG(JPEG)，PNG"
    assert type(content) is bytes, "文件流应该是Bytes类型吧？"+str(content)
    # 先存到临时的文件待检测
    fake_path = os.path.join(TEMP_PATH, username+'_tmp'+suffix)
    print(f'将上传图片写入临时文件夹：{fake_path}')
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

    data = {"api_key": FACE_SECRET_KEY['key'],
            "api_secret": FACE_SECRET_KEY['secret']}

    try:
        with open(img_path, 'rb') as f:
            response = face_post(face_api_url, data=data,
                                 files={"image_file": f})
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

    data = {"api_key": FACE_SECRET_KEY['key'],
            "api_secret": FACE_SECRET_KEY['secret']}

    files = {"image_file1": file_buffer_1, "image_file2": file_buffer_2}

    response = face_post(face_api_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    if 'confidence' in req_dict.keys():
        return req_dict['confidence']
    else:
        return None


# 人脸识别部分
@async_exception_handler
async def face_recognition(file: UploadFile):
    r"""
    人脸登录，用于比较人脸信息
    file，传进来的照片文件
    """
    # 处理传进来的照片
    suffix = '.'+file.filename.split('.')[-1]
    assert suffix == '.jpg' or suffix == '.jpeg' or suffix == '.png', "只支持JPG(JPEG)，PNG"
    content = await file.read()
    assert type(content) is bytes, "文件流应该是Bytes类型吧？"+str(content)
    print(f"将临时图片存到：{os.path.join(TEMP_PATH, 'temp'+suffix)}待检测")
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
                        user_check =  user_check[0]
                        access_token_expires = timedelta(
                            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                        access_token = create_access_token(
                            data={"sub": str(user_check['username'])+':'+str(user_check['status'])}, expires_delta=access_token_expires
                        )
                        return {'message': 'success', 'data': user_check, "access_token": access_token, "token_type": "bearer"}
                        
    raise HTTPException(status_code=400, detail="未匹配到人脸信息")


def has_face(username: str):
    r"""
    判断人脸信息是否注册
    """
    if os.path.exists(os.path.join(FACE_PATH, username+'.jpg')) or \
        os.path.exists(os.path.join(FACE_PATH, username+'.jpeg')) or \
            os.path.exists(os.path.join(FACE_PATH, username+'.png')):
        return 1
    else:
        return 0


# 密码登录部分

def hash_password(password: str, salt: str = "lxh"):
    r"""
    hd5加密密码
    """
    user_hash = md5()
    user_hash.update((password+salt).encode(encoding='utf-8'))
    return user_hash.hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    r"""
    生成一个jwt密钥
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@exception_handler
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名不存在", headers={"WWW-Authenticate": "Bearer"})
    else:
        user_check = user_check[0]
        if user_check['password'] != hash_password(password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="密码错误", headers={"WWW-Authenticate": "Bearer"})
    del user_check['password']
    user_check['has_face'] = has_face(username)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user_check['username'])+':'+str(user_check['status'])}, expires_delta=access_token_expires
    )
    return {'message': 'success', 'data': user_check, "access_token": access_token, "token_type": "bearer"}
