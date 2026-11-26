from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.tasks import Task
from schemas.tasks import TasksUpdate


async def create(db: AsyncSession, title: str, description: str,state: str, owner_id: int):
    task_data = {
        "title": title,
        "description": description,
        "state": state,
        "owner_id": owner_id
    }
    task = Task(**task_data) # type: ignore
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_by_title(db: AsyncSession, title: str):
    result = await db.execute(select(Task).where(Task.title == title))
    return result.scalars().one_or_none()

async def get_all_task(db: AsyncSession,user_id: int):
    result = await db.execute(select(Task).where(Task.owner_id == user_id))
    return result.scalars().all()

async def get_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()

async def update(db: AsyncSession, payload: TasksUpdate, task: Task):
    for k,v in payload.model_dump(exclude_unset=True).items():
        setattr(task, k, v)
    await db.commit()
    await db.refresh(task)
    return task

async def delete(db: AsyncSession, task_id: int) -> None:
    task = await db.get(Task, task_id)
    print("***************",task)
    await db.delete(task)
    await db.commit()
    return None