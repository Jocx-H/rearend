#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI
from api import user_api, job_api, dept_api, notice_api, document_api
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# 声明fastapi的实例
app = FastAPI()
# 配置静态资源的存放路径以及请求的路径
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# 跨域配置
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


# 注册api模块
# app.include_router(job_api.router)
# app.include_router(user_api.router)
# app.include_router(notice_api.router)
# app.include_router(document_api.router)
app.include_router(dept_api.router, prefix='/api')

# 配置容器启动相应的实例
if __name__ == '__main__':
    uvicorn.run(app='main:app', port=8000, reload=True)
