#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _io import BufferedReader
from json import JSONDecoder
from os.path import exists as file_exists
from os import remove as file_remove
from fastapi import UploadFile
from requests import post as face_post
from dao import crud
from typing import Optional, BinaryIO, Union

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


def detect_face(img_path: str) -> bool:
    r"""
    检测注册的图片是否是人脸
    """
    face_api_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"

    data = {"api_key": __all__['key'],
            "api_secret": __all__['secret']}

    files = {"image_file": open(img_path, 'rb')}

    try:
        response = face_post(face_api_url, data=data, files=files)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        if req_dict['faces'] is None:  # 如果不是人脸则`req_dict[face]`是None
            return False
        return True
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
    path = "assets/private/face_img/"
    usernames = crud.select_items('user_inf',
                                  columns=['username'])
    for user in usernames:
        if file_exists(path + user['username'] + '.jpg'):  # 判断文件是否存在
            compared_img = open(
                path + user['username'] + '.jpg', "rb")  # TODO 这不一定是jpg啊
            res = compare_face(compared_img, img)
            if res:
                return True
        else:
            continue
    else:
        return False


def face_add(content: Union[bytes, str], username: str) -> bool:
    r"""
    注册人脸
    """
    # 先把数据流存成图片再检测
    path = "assets/private/face_img/"  # 待存人脸图片的地址
    face_path = path + username + '.jpg'
    with open(face_path, 'wb') as f:
        f.write(content)
    res = detect_face(face_path)
    if not res:  # 如果不是人脸就删除图片
        file_remove(face_path)
    return res