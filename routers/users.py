from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_get_db
from dependencies.utils import limiter, get_current_user
from schemas.users import UserOut, UserCreate, UserUpdate
from services import user_service
from fastapi import Request

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut, status_code=201)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(async_get_db)):
    return await user_service.register_user(db, payload)

@router.get("/",response_model=list[UserOut])
@limiter.limit("5/minute")              # 每分钟最多 5 次
async def list_users(request: Request,_ = Depends(get_current_user),db: AsyncSession = Depends(async_get_db)):
    return await user_service.get_all_user(db)

@router.put("/user/{user_id}")
async def modify_user(user_id: int, payload: UserUpdate,db: AsyncSession = Depends(async_get_db)):
    return await user_service.update_user(db, payload, user_id)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(async_get_db)):
    return await user_service.get_user_by_id(db, user_id)

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(async_get_db)):
    return await user_service.delete_user(db, user_id)