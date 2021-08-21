#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 内嵌于有效键里面的服务

from fastapi.responses import JSONResponse
from dao import user_dao

def get_user_infos(uname):
    r'''
    '''
    # 1.就是做需求的逻辑操作(对数据的处理 可能涉及到持久化层 这个数据不一定要入库的)
    data = user_dao.select_users(uname)
    # 2.由服务做相应的数据反馈
    return JSONResponse(
        content={
            'code': 200,
            'data': {
                'users': data
            },
            'message': "数据获取成功"
        }
    )


def buy_product_service(product):
    r'''
    1.下订单
    2.减库存
    '''
    pass
