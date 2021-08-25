#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 引入路由管理
from fastapi import APIRouter, Query, HTTPException
from model.code import Code400
from model.user import User
from service import user_service
from fastapi.encoders import jsonable_encoder
# 构建api路由
router = APIRouter(
    prefix="/user",
    tags=["User"],
)

