#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Notice(BaseModel):
    r"""
    更新公告信息使用的模型
    """
    title: str = Field(None, min_length=1, max_length=50)
    content: Optional[str] = Field(None, max_length=300)
    create_time: Optional[datetime] = None
    username: str = Field(None, min_length=1, max_length=20,
                          description="The username of notifier")
