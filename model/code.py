#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseModel


class Code400(BaseModel):
    detail: str = "Bad Request(客户端语法错误)"
