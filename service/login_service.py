#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, BinaryIO, Union
from requests import post as face_post
from fastapi import UploadFile
from json import JSONDecoder
from _io import BufferedReader
from hashlib import md5
from dao import crud
from fastapi import HTTPException
import os


FACE_PATH = "assets/private/face_img"
__all__ = {
    "key": "iXWmKDAuviqmnDx9KcGcb5f26VXD8qro",
    "secret": "aDChdAEjL4hY5AYfshQL1rW4DhUVzyWu"
}  # 密钥

threshold = 70  # 人脸识别通过的阈值
temp_path = "assets/private/temp.jpg"



def get_face():
    r"""
    从数据库里面获取人脸图像的相对位置
    """
    pass


def compare_face(file_buffer_1: BinaryIO, file_buffer_2: BinaryIO) -> bool:
    r"""
    比较人脸
    """
    face_api_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"

    data = {"api_key": __all__['key'],
            "api_secret": __all__['secret']}

    files = {"image_file1": file_buffer_1, "image_file2": file_buffer_2}

    try:
        response = face_post(face_api_url, data=data, files=files)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        res = req_dict['confidence']
        if res > threshold:
            return True
        return False
    except Exception as e:
        print(e)
        return False


def face_recognition(content: Union[bytes, str]) -> bool:
    r"""
    人脸登录，用于比较人脸信息
    """
    # 处理传进来的照片
    with open(temp_path, 'wb') as f:
        f.write(content)
    img = open(temp_path, 'rb')

    # 处理已存图片
    
    usernames = crud.select_items('user_inf',
                                  columns=['username'],
                                  where={'face_path': FACE_PATH})
    for user in usernames:
        compared_img = open(
            os.path.join(FACE_PATH, user['username'] + '.jpg'), "rb")  # TODO 这不一定是jpg啊
        res = compare_face(compared_img, img)
        if res:
            return True
    else:
        return False


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
             'qq_num', 'email', 'party', 'birthday', 'race',
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
    return user_check
