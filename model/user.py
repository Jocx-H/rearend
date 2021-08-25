#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from datetime import datetime
from enum import Enum


class Status(int, Enum):
    administrator = 1
    normal_user = 2


class UserAuthority(BaseModel):
    r"""
    鉴权时用的模型，修改密码，人脸验证等都要用到
    """
    # username: str = Field(..., min_length=1, max_length=20)
    password: str = Field(..., min_length=6, max_length=32)
    status: Status = Field(
        Status.normal_user,
        description="1 represent administrator and 2 represent normal user")
    face_url: Optional[HttpUrl] = Field(None)  # max_length=255
    # face_path: Optional[str] = Field(None, max_length=255)


class Sex(int, Enum):
    man = 1
    woman = 2


class UserInfo(BaseModel):
    r"""
    更新用户信息时使用的模型
    """
    # username: str = Field(..., min_length=1, max_length=20)
    avatar_path: Optional[str] = Field(None, max_length=255)
    department: Optional[str] = Field(None, min_length=1, max_length=50)
    job: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=20)
    card_id: Optional[str] = Field(None, min_length=18, max_length=18)
    address: Optional[str] = Field(None, min_length=1, max_length=50)
    post_code: Optional[str] = Field(None, min_length=1, max_length=50)
    tel: Optional[str] = Field(None, min_length=1, max_length=16)
    phone: Optional[str] = Field(None, min_length=1, max_length=11)
    qq_num: Optional[str] = Field(None, min_length=1, max_length=10)
    email: Optional[EmailStr] = Field(None)  # min_length=1, max_length=50
    sex: Optional[Sex] = None
    party: Optional[str] = Field(None, min_length=1, max_length=10)
    birthday: Optional[datetime] = None
    race: Optional[str] = Field(None, min_length=1, max_length=100)
    education: Optional[str] = Field(None, min_length=1, max_length=10)
    speciality: Optional[str] = Field(None, min_length=1, max_length=10)
    hobby: Optional[str] = Field(None, min_length=1, max_length=100)
    remark: Optional[str] = Field(None, min_length=1, max_length=500)
    create_date: Optional[datetime] = None


class User(BaseModel):
    r"""
    创建用户时使用的模型
    """
    username: str = Field(..., min_length=1, max_length=20)
    authority: UserAuthority
    info: UserInfo
