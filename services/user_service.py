from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from repositories import user_repo
from schemas.users import UserCreate, UserUpdate


async def register_user(db: AsyncSession, payload: UserCreate) -> User:
    if await user_repo.get_by_username(db, payload.username):
        raise HTTPException(409, "用户名已存在")  # 业务规则
    return await user_repo.create(db, payload.username, payload.password,payload.email, payload.age)

async def get_all_user(db: AsyncSession):
    return await user_repo.get_all(db)

async def get_user_by_id(db: AsyncSession, user_id: int):
    user = await user_repo.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

async def update_user(db: AsyncSession, payload: UserUpdate, user_id: int) -> User:
    user = await user_repo.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return await user_repo.update(db, payload, user)

async def delete_user(db: AsyncSession, user_id: int):
    user = await user_repo.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return await user_repo.delete(db, user_id)
