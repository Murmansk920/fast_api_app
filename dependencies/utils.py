from datetime import datetime, timezone, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette import status

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Swagger 登录入口
limiter = Limiter(key_func=get_remote_address)   # 按客户端 IP 限流

def hash_password(password: str) -> str:
    return pwd_context.hash(password)      # 注册时调用，存入数据库

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)  # 登录时调用

# ---------- 当前用户依赖（认证） ----------
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        user_id = payload.get("id")
        if user_id is None:
            raise ValueError
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效或过期的 token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": username, "user_id": user_id}

# ---------- 角色权限依赖（授权） ----------
def require_admin(user: str = Depends(get_current_user)):
    if user != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "权限不足")
    return user

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload.update({"exp": expire})   # 关键：必须带过期时间
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def refresh_token(payload: dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=7200)
    payload.update({"exp": expire})   # 关键：必须带过期时间
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

