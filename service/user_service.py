#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.user import User, Status
from dao import crud
from typing import Optional, Dict, Union, List
from service.login_service import hash_password
from fastapi import UploadFile
import os
from api.utils import exception_handler, async_exception_handler
from fastapi.encoders import jsonable_encoder

AVATAR_PATH = 'assets/public/avatar'
AVATAR_URL = 'resources/avatar'


# def decode_info(info: dict):
#     r"""
#     将dict里面的内容全部解码成数据库接受的格式，被jsonable_encoder代替
#     """
#     enums = set(['sex', 'status'])
#     times = set(['birthday', 'create_time'])
#     special_strs = ['EmailStr', 'face_url', 'avatar_url']
#     for i in info.keys():
#         if info[i] is None:
#             pass
#         elif i in enums:
#             info[i] = info[i].value
#         elif i in times:
#             info[i] = info[i].strftime("%Y-%m-%d %H:%M:%S")
#         elif i in special_strs:
#             info[i] = str(info[i])
#         assert type(info[i]) == str or type(info[i]) == int \
#             or type(info[i]) == float or type(info[i] is None)
#     return info


@async_exception_handler
async def change_avatar(file: UploadFile,
                        username: str):
    r"""
    修改用户的头像，以路径参数username指定用户
    """
    content = await file.read()
    filename = username+'_avatar.'+file.filename.split('.')[-1]
    assert type(content) is bytes, "文件流应该是Bytes类型吧？"+str(content)
    print(f"将上传头像写入：{os.path.join(AVATAR_PATH, filename)}")
    with open(os.path.join(AVATAR_PATH, filename), 'wb') as f:
        f.write(content)
    return {'message': crud.update_items('user_inf', {'avatar_url': os.path.join(AVATAR_URL, filename)},
                                         where={'username': username}),
            'data': {'avatar_url': os.path.join(AVATAR_URL, filename)}}


@exception_handler
def add_user(user: User) -> str:
    r"""
    添加员工
    """
    assert user.username is not None, "必须传入username"
    if user.password is None:
        user.password = "123456"
    if user.status is None:
        user.status = Status.normal_user  # 未指定权限则默认为普通用户
    user_dict = jsonable_encoder(user.dict())
    user_dict['password'] = hash_password(user_dict['password'])
    columns = []
    values = []
    for k in user_dict.keys():
        if user_dict[k] is not None:
            columns.append(k)
            values.append(user_dict[k])
    return crud.insert_items("user_inf", columns=columns, values=[values])

@exception_handler
def remove_user(username: Optional[str]) -> str:
    r"""
    删除员工，以username为唯一指定目标
    """
    if username is None:
        return crud.delete_items('user_inf', where=None)
    else:
        return crud.delete_items('user_inf', where={'username': username})

@exception_handler
def update_user(username: Optional[str], user: User) -> str:
    r"""
    更新员工的信息，以username为唯一指定目标
    """
    items = user.dict(exclude_unset=True)
    items = jsonable_encoder(items)
    items = {k: v for k, v in items.items() if v is not None}
    if 'password' in items.keys():
        items['password'] = hash_password(items['password'])
    if username is None:
        return crud.update_items('user_inf', items, where=None)
    else:
        return crud.update_items('user_inf', items, where={'username': username})

@exception_handler
def get_user(where: Optional[Dict[str, Union[str, int, float]]],
             limit: Optional[int],
             skip: int) -> List[Dict[str, Union[str, int, float]]]:
    r"""
    获取员工的信息，提供三种查询模式：
        1. 从数据库第一条开始返回条目
        2. 根据username查询直接访问一位员工
        3. 返回符合where条件的员工
    """
    if where is None:
        return crud.select_items('user_inf', where=None, limit=limit, skip=skip)
    else:
        # 去除字典中值为None的键
        where = {k: v for k, v in where.items() if v is not None}
        where = jsonable_encoder(where)
        return crud.select_items('user_inf', where=where, limit=limit, skip=skip)
