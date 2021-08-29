import traceback
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from functools import wraps


def try_catch_exception(func):
    @wraps(func)
    def try_catch(*args, **kwargs):
        try:
            # assert user.username is not None, "必须传入username"
            # if user.password is None:
            #     user.password = "123456"
            result = func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise HTTPException(
                status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
        return jsonable_encoder(result)
    return try_catch

# if __name__ == '__main__':
#     @try_catch_exception
#     def haha(a, b):
#         raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")


#     print(haha(1, 2))
