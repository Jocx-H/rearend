#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 引入路由管理
from fastapi import APIRouter
from service import job_service

# 构建api路由
router = APIRouter(
    prefix="/job",
    tags=["job"],
)


# @router.get("/getjobs")
# async def get_jobs(uname: str):
#     r"""
#     获取用户的信息数据
#     """
#     print(uname)
#     # 1.通过调用相应的服务得到对应的反馈
#     return job_service.get_job_infos(uname)
