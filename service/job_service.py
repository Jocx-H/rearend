#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.job import Job
from dao import crud
from typing import Optional, List, Dict, Union


def add_job(job: Job) -> str:
    r"""
    添加职位，name必选，remark可选
    """
    job_dict = job.dict()
    columns = []
    values = []
    for k in job_dict.keys():
        columns.append(k)
        values.append(job_dict[k])
    return crud.insert_items("job_inf", columns=columns, values=[values])


def remove_job(name: Optional[str]) -> str:
    r"""
    删除职位，以路径参数name唯一指定
    """
    if name is None:
        return crud.delete_items('job_inf', where=None)
    else:
        return crud.delete_items('job_inf', where={'name': name})


def get_job(name: Optional[str], limit: Optional[int], skip: int) -> List[Dict[str, Union[str, int, float]]]:
    r"""
    获取职位的信息，以路径参数name唯一指定，可以选择limit和skip
    """
    if name is None:
        return crud.select_items('job_inf', columns=['name', 'remark'],
                                 where=None, limit=limit, skip=skip)
    else:
        return crud.select_items('job_inf', columns=['name', 'remark'],
                                where={'name': name}, limit=limit, skip=skip)


def update_job(name: Optional[str], job: Job) ->str:
    r"""
    更新职位的信息，以传入的name唯一指定，可选修改name和remark
    """
    items = job.dict(exclude_unset=True)
    if name is None:
        return crud.update_items('job_inf', items, where=None)
    else:
        return crud.update_items('job_inf', items, where={'name': name})
