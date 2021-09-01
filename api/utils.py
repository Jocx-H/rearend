from datetime import datetime, timedelta
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Optional
import traceback
from fastapi import HTTPException
from functools import wraps

ALGORITHM = "HS256"  # jwt加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # token有效时间
SECRET_KEY = "277b0e48a7355e18456742dfe401ac2a501713566b0d2da873e74d69cda2c692"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/passwd")


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         sub = payload.get("sub")
#         username: str = sub.split(':')[0:-1]
#         status: int = int(sub.split(':')[-1])
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_admin_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


def exception_handler(func):
    r"""
    封装try catch步骤，针对同步函数
    """
    @wraps(func)
    def try_catch(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
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
            result = await func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise HTTPException(
                status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
        return result
    return try_catch
