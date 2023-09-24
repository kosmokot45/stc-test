from typing import Iterable
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import TaskCreate, TaskUpdate, LastEndpoint
from core.models import Task
from core.models import Worker


async def get_tasks(db: AsyncSession) -> list[Task]:
    query = select(Task)
    result: Result = await db.execute(query)
    tasks = result.scalars().all()
    return list(tasks)


async def get_workers_todo(db: AsyncSession):  # -> list[Task]:

    final_result: list[LastEndpoint] = []
    # Take priority tasks
    query = select(Task).options(selectinload(Task.parent)).filter(Task.status=="in progress", Task.parent.has(Task.status=="not in progress"))
    tasks: Iterable[Task]= await db.scalars(query)
    # Find workers and collect final list
    query = select(Worker).options(selectinload(Worker.tasks))
    workers: Iterable[Worker] = await db.scalars(query)
    
    workers_tasks: dict[int, int] = {worker.id:len(worker.tasks) for worker in workers}
    for task in tasks:
        free_worker_id: int = min(workers_tasks, key=workers_tasks.get)
        priority: int = workers_tasks[task.worker_id] - workers_tasks[free_worker_id]
        worker: Worker = await db.get(Worker, task.worker_id) if priority <= 2 else await db.get(Worker, free_worker_id)
        final_result.append({'Task': task.parent.name, 'Deadline': str(task.parent.deadline), 'Worker': worker.name})
        
    return JSONResponse(content=final_result)



async def get_task(db: AsyncSession, task_id: int) -> Task | None:
    return await db.get(Task, task_id)


async def create_task(db: AsyncSession, task_create: TaskCreate) -> Task:
    task=Task(**task_create.model_dump())
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
