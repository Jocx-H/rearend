#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from datetime import date, datetime
from enum import Enum


class Status(int, Enum):
    administrator = 1
    normal_user = 2


class Sex(int, Enum):
    man = 1
    woman = 2


class User(BaseModel):
    r"""
    创建用户时使用的模型
    """
    username: str = Field(None, min_length=1, max_length=20)
    password: str = Field(None, min_length=1, max_length=20)
    status: Status = Field(None,
                           description="1 represent administrator and 2 represent normal user")
    name: Optional[str] = Field(None, min_length=1, max_length=20)
    sex: Optional[Sex] = None
    card_id: Optional[str] = Field(None, min_length=18, max_length=18)
    avatar_url: Optional[HttpUrl] = Field(None)  # max_length=255
    department: Optional[str] = Field(None, min_length=1, max_length=50)
    job: Optional[str] = Field(None, min_length=1, max_length=50)
    address: Optional[str] = Field(None, min_length=1, max_length=50)
    post_code: Optional[str] = Field(None, min_length=6, max_length=6)
    tel: Optional[str] = Field(None, min_length=1, max_length=16)
    phone: Optional[str] = Field(None, min_length=1, max_length=11)
    qq_num: Optional[str] = Field(None, min_length=6, max_length=12)
    email: Optional[EmailStr] = Field(None)
    party: Optional[str] = Field(None, min_length=1, max_length=10)
    birthday: Optional[date] = None
    nationality: Optional[str] = Field(None, min_length=1, max_length=100)
    education: Optional[str] = Field(None, min_length=1, max_length=10)
    speciality: Optional[str] = Field(None, min_length=1, max_length=10)
    hobby: Optional[str] = Field(None, min_length=1, max_length=100)
    remark: Optional[str] = Field(None, min_length=1, max_length=500)
    create_time: Optional[datetime] = None
    face_url: Optional[HttpUrl] = Field(None)  # max_length=255
