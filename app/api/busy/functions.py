from typing import Iterable
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import LastEndpoint
from app.core.models import Task
from app.core.models import Worker


async def get_workers_todo(db: AsyncSession):# -> list[LastEndpoint]:

    final_result: list[LastEndpoint] = []
    # Take priority tasks
    query = select(Task).options(selectinload(Task.child)).filter(Task.status=="in progress", Task.child.has(Task.status=="not in progress"))
    tasks: Iterable[Task]= await db.scalars(query)
    # Find workers and collect final list
    query = select(Worker).options(selectinload(Worker.tasks))
    workers: Iterable[Worker] = await db.scalars(query)
    
    workers_tasks: dict[int, int] = {worker.id:len(worker.tasks) for worker in workers}
    for task in tasks:
        free_worker_id: int = min(workers_tasks, key=workers_tasks.get) # type: ignore
        priority: int = workers_tasks[task.worker_id] - workers_tasks[free_worker_id] # type: ignore
        worker: Worker = await db.get(Worker, task.worker_id) if priority <= 2 else await db.get(Worker, free_worker_id) # type: ignore
        final_result.append({'Task': task.name, 'Deadline': str(task.child.deadline), 'Worker': worker.name}) # type: ignore
    
    # print(final_result)
    # return final_result
    return JSONResponse(content=final_result)


async def get_workers_with_tasks(db: AsyncSession):
    query = select(Worker).options(selectinload(Worker.tasks))
    workers: Iterable[Worker] = await db.scalars(query)

    worker_dict = [
        jsonable_encoder(worker) for worker in workers]

    for worker in worker_dict:
        worker["task_count"] = len(worker["tasks"])

    worker_dict.sort(key=lambda cnt: cnt["task_count"], reverse=True)

    for worker in worker_dict:
        worker.pop("task_count")

    return JSONResponse(content=worker_dict)