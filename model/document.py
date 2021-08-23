#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Document(BaseModel):
    r"""
    创建和更新部门信息使用的模型
    """
    title: str = Field(None, min_length=1, max_length=50)
    filename: str = Field(None, min_length=1, max_length=300)
    remark: Optional[str] = Field(None, max_length=300)
    create_time: Optional[datetime] = None
    username: str = Field(..., min_length=1, max_length=20,
                          description="The username of uploader")
