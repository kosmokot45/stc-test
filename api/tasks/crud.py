from typing import Iterable
from sqlalchemy import select, func
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import TaskCreate, TaskUpdate
from core.models import Task


async def get_tasks(db: AsyncSession) -> list[Task]:
    query = select(Task)
    result: Result = await db.execute(query)
    tasks = result.scalars().all()
    return list(tasks)


async def get_workers_todo(db: AsyncSession):
    query = select(Task)
    result: Iterable[Task] = await db.scalars(query)
    tasks_full: list[Task] = [
        jsonable_encoder(task) for task in result]
    tasks: list[Task] = []
    parent_workers: list[int] = []
    for task in tasks_full:
        if task["status"] == "in progress" and task["parent"] != None and task["parent"]["status"] == "not in progress":  # type: ignore
            tasks.append(task["parent"])  # type: ignore
            # parent_workers.append(task["parent"]["worker_id"])  # type: ignore
            query = select(func.count("*")).select_from(Task).where(
                Task.worker_id == task["worker_id"])
            result_w: Result = await db.execute(query)
            cnt = result_w.all()[0][0]
            print("******")
            print(cnt, task["worker_id"])
            print("******")
            if cnt >= 6:
                parent_workers.append(task["worker_id"])
            else:
                parent_workers.append(1)
    print(parent_workers)
    # print("******")
    # print(result_w.all()[0][0])
    # print("******")
    # найти наименее загруженного
    ...
    # посчтитать по тем таскам сколько задач
    # print(parent_workers)
    # query = select(Task).where(Task.worker_id.in_(parent_workers))
    # result: Iterable[Task] = await db.scalars(query)
    return JSONResponse(content=tasks)
    return query


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
