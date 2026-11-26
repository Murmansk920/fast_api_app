from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from werkzeug.security import check_password_hash

from db import async_get_db
from fastapi import Request
from dependencies.utils import create_access_token, limiter, refresh_token
from repositories.user_repo import get_by_username

router = APIRouter(prefix="/auth", tags=["鉴权"])

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request,form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(async_get_db)):
    user = await get_by_username(db, form_data.username)
    if user is None or not check_password_hash(user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    token = create_access_token({"sub": form_data.username,"id": user.id})
    return {"access_token": token, "token_type": "bearer"}