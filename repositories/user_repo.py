from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import generate_password_hash

from models.users import User
from schemas.users import UserUpdate


async def create(db: AsyncSession, username: str, password: str,email: str, age: int | None) -> User:
    user = User(username=username, password= generate_password_hash(password),email = email, age=age)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().one_or_none()

async def get_all(db: AsyncSession) -> Sequence[Any]:
    result = await db.execute(select(User))
    return result.scalars().all()

async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def update(db: AsyncSession, payload: UserUpdate, user: User) -> User:
    for k,v in payload.model_dump(exclude_unset=True).items():
        setattr(user, k, v)
    await db.commit()
    await db.refresh(user)
    return user

async def delete(db: AsyncSession, user_id: int) -> None:
    user = await db.get(User, user_id)
    await db.delete(user)
    await db.commit()
    return None