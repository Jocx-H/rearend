#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from fastapi import APIRouter, Path, Query, Depends
from model.job import Job
from model.code import Code400
from service import job_service
from api.utils import check_current_user, check_current_admin_user
from typing import Optional
import asyncio

# 构建api路由
router = APIRouter(
    prefix="/job",
    tags=["Job"],
)


@router.post("/add", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_admin_user)])
async def add_job(job: Job):
    r"""
    添加职位，name必选，remark可选
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, job_service.add_job, job)
    

@router.delete("/remove-all", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_admin_user)])
async def remove_all_jobs():
    r"""
    删除所有职位
    注意在删除职位时要保证没有员工在这个职位，否则无法删除
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, job_service.remove_job, None)
    

@router.delete("/remove/{name}", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_admin_user)])
async def remove_job(name: str = Path(..., min_length=1, max_length=50)):
    r"""
    删除职位，以路径参数name唯一指定
    ，注意在删除职位时要保证没有员工在这个职位，否则无法删除
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, job_service.remove_job, name)
    

@router.get("/get-all", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_user)])
async def get_all_jobs(limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取所有职位的信息
    可以选择limit和skip
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, job_service.get_job, None, limit, skip)
    

@router.get("/get/{name}", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_user)])
async def get_job(name: str = Path(..., min_length=1, max_length=50),
                  limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取职位的信息，以路径参数name唯一指定，可以选择limit和skip
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, job_service.get_job, name, limit, skip)
    

@router.put("/update-all", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_admin_user)])
async def update_all_jobs(job: Job):
    r"""
    更新职位的信息，以传入的路径参数name唯一指定，可选修改name和remark
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, job_service.update_job, None, job)
    

@router.put("/update/{name}", responses={400: {"model": Code400}}, dependencies=[Depends(check_current_admin_user)])
async def update_job(job: Job,
                     name: str = Path(..., min_length=1, max_length=50)):
    r"""
    更新职位的信息，以传入的路径参数name唯一指定，可选修改name和remark
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, job_service.update_job, name, job)
    
