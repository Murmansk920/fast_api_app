from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import async_get_db
from fastapi import Request
from dependencies.utils import get_current_user, limiter
from schemas.tasks import TaskCreate, TasksOut, TasksUpdate
from services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model = TasksOut,status_code=201)
async def create_task(payload: TaskCreate,user_dict = Depends(get_current_user), db: AsyncSession = Depends(async_get_db)):
    return await task_service.create_task(db, payload,user_dict.get("user_id",None))

@router.get("/", response_model=list[TasksOut])
@limiter.limit("5/minute")              # 每分钟最多 5 次
async def list_tasks(request: Request,user_dict = Depends(get_current_user),db: AsyncSession = Depends(async_get_db)):
    return await task_service.get_all_tasks(db,user_dict.get("user_id",None))

@router.put("/{task_id}")
async def modify_task(task_id:int, payload: TasksUpdate,user_dict = Depends(get_current_user), db: AsyncSession = Depends(async_get_db)):
    return await task_service.update_task(db, payload, user_dict.get("user_id",None),task_id)

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int ,user_dict = Depends(get_current_user), db: AsyncSession = Depends(async_get_db)):
    return await task_service.delete_task(db, task_id,user_dict.get("user_id",None))