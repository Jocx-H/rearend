#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseModel


class Code400(BaseModel):
    detail: str = "客户端语法错误"

class Code403(BaseModel):
    detail: str="客户端请求权限不足"
