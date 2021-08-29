import traceback
from fastapi import HTTPException
from functools import wraps
import asyncio


def exception_handler(func):
    r"""
    封装try catch步骤，针对同步函数
    """
    @wraps(func)
    def try_catch(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # loop = asyncio.get_event_loop()
            # result = await loop.run_in_executor(None, func, *args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise HTTPException(
                status_code=400, detail="客户端运行错误，错误原因："+str(repr(e))+" 请检查输入内容或联系管理员！")
        return result
    return try_catch


def async_exception_handler(func):
    r"""
    封装try catch步骤，针对异步函数
    """
    @wraps(func)
    async def try_catch(*args, **kwargs):
        try:
            result=await func(*args, **kwargs)
            # loop = asyncio.get_event_loop()
            # result = await loop.run_in_executor(None, func, *args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise HTTPException(
                status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
        return result
    return try_catch

# if __name__ == '__main__':
#     @try_catch_exception
#     def haha(a, b):
#         raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")


#     print(haha(1, 2))
