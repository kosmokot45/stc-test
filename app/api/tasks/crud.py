from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import TaskCreate, TaskUpdate
from app.core.models import Task


async def get_tasks(db: AsyncSession) -> list[Task]:
    query = select(Task)
    result: Result = await db.execute(query)
    tasks = result.scalars().all()
    return list(tasks)


async def get_task(db: AsyncSession, task_id: int) -> Task | None:
    return await db.get(Task, task_id)


async def create_task(db: AsyncSession, task_create: TaskCreate) -> Task:
    task = Task(**task_create.model_dump())
    db.add(task)
    await db.commit()
    return task


async def update_task(db: AsyncSession, task: Task, task_update: TaskUpdate) -> Task:
    for key, value in task_update.model_dump().items():
        setattr(task, key, value)
    await db.commit()
    return task


async def delete_task(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.commit()
