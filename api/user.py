# 引入路由管理
from fastapi import APIRouter
# 让数据以json的格式返回
from fastapi.responses import JSONResponse

from service import userService

# 构建api路由
router = APIRouter()

## 获取用户的信息数据
@router.get("/getUsers",tags=["用户"])
async def getusers(uname:str):
        print(uname)
    ### 1.通过调用相应的服务得到对应的反馈
        return userService.getUserInfos(uname)
    
 
