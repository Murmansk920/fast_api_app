from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import task_repo
from schemas.tasks import TaskCreate, TasksUpdate


async def create_task(db: AsyncSession, payload: TaskCreate, user_id: int):
    if await task_repo.get_by_title(db, payload.title):
        raise HTTPException(409, "任务已存在")  # 业务规则
    return await task_repo.create(db, payload.title, payload.description,payload.state, user_id)

async def get_all_tasks(db: AsyncSession,user_id: int | None):
    if user_id is None:
        return HTTPException(status_code=404, detail="未鉴权")
    return await task_repo.get_all_task(db,user_id)

async def update_task(db: AsyncSession, payload: TasksUpdate, user_id: int,task_id:int):
    task = await task_repo.get_by_id(db, task_id)
    if task is None or task.owner_id != user_id:
        raise HTTPException(status_code=404, detail="任务不存在")
    return await task_repo.update(db, payload, task)

async def delete_task(db: AsyncSession, task_id: int, user_id: int):
    task = await task_repo.get_by_id(db, task_id)
    if task is None or task.owner_id != user_id:
        raise HTTPException(status_code=404, detail="任务不存在")
    return await task_repo.delete(db, task_id)