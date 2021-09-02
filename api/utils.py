from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import traceback
from fastapi import HTTPException
from functools import wraps
import json

# 读取本地安全配置
with open("config.json") as f:
    db_configs = json.load(f)['safe']

SECRET_KEY = db_configs['secret_key']
ALGORITHM = db_configs['jwt_algorithm']  # jwt加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = db_configs['access_token_expire_minutes']  # token有效时间
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/passwd")


async def check_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = str(payload.get("sub"))
        username = sub.split(':')[0:-1]
        admin_status = sub.split(':')[-1]
        if username is None or status is None:
            raise credentials_exception
        # token_data = {'username':username, 'status': int(admin_status)}
    except JWTError:
        raise credentials_exception
    return int(admin_status) == 1


async def check_current_admin_user(is_admin: bool = Depends(check_current_user)):
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="没有管理员权限",
            headers={"WWW-Authenticate": "Bearer"},
        )


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
