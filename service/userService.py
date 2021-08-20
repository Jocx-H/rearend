# 服务层当中,服务是不能命名为数据库的操作名字
from fastapi.responses import JSONResponse
from dao import userDao

def  getUserInfos(uname):
    ## 1.就是做需求的逻辑操作(对数据的处理 可能涉及到持久化层 这个数据不一定要入库的)
        data = userDao.selectUsers(uname)
    ## 2.由服务做相应的数据反馈
        return JSONResponse(
        content={
            'code': 200,
            'data': {
                'users':data
            },
            'message': "数据获取成功"     
        }
    )


def  buyProductService(Product):
    ## 1.下订单
    ## 2.减库存
        pass