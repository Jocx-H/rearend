#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 引入路由管理
from fastapi import APIRouter
from service import document_service

# 构建api路由
router = APIRouter(
    prefix="/document",
    tags=["Document"],
)


