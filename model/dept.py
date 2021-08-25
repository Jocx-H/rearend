#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field


class Department(BaseModel):
    r"""
    创建和更新部门信息使用的模型
    """
    name: str = Field(None, min_length=1, max_length=50)
    remark: Optional[str] = Field(None, max_length=300)
