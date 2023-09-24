from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.workers.schemas import WorkerCreate
from api.workers.crud import create_worker
from api.tasks.schemas import TaskCreate
from api.tasks.crud import create_task
from core.models.database import database
from datetime import date


workers: list[WorkerCreate] = [
    WorkerCreate(name="Marina", role="admin"),
    WorkerCreate(name="Vladimir", role="coder"),
    WorkerCreate(name="Polina", role="coder"),
    WorkerCreate(name="Narek", role="coder"),
    WorkerCreate(name="Daniil", role="admin"),
]


tasks: list[TaskCreate] = [
    TaskCreate(name="task_1", deadline=date(2024, 1, 1), status="in progress",      parent_id=None, worker_id=1),
    TaskCreate(name="task_2", deadline=date(2024, 1, 1), status="in progress",      parent_id=None, worker_id=2),
    TaskCreate(name="task_3", deadline=date(2024, 1, 1), status="in progress",      parent_id=2,    worker_id=3),
    TaskCreate(name="task_4", deadline=date(2024, 1, 1), status="in progress",      parent_id=1,    worker_id=1),
    TaskCreate(name="task_5", deadline=date(2024, 1, 1), status="done",             parent_id=None, worker_id=2),
    TaskCreate(name="task_6", deadline=date(2024, 1, 1), status="in progress",      parent_id=None, worker_id=4),
    TaskCreate(name="task_7", deadline=date(2024, 1, 1), status="in progress",      parent_id=1,    worker_id=3),
    TaskCreate(name="task_8", deadline=date(2024, 1, 1), status="in progress",      parent_id=7,    worker_id=1),
    TaskCreate(name="task_9", deadline=date(2024, 1, 1), status="in progress",      parent_id=None, worker_id=5),
    TaskCreate(name="task_10", deadline=date(2024, 1, 1), status="in progress",     parent_id=9,    worker_id=2),
    TaskCreate(name="task_11", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=3),
    TaskCreate(name="task_12", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=5),
    TaskCreate(name="task_13", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=2),
    TaskCreate(name="task_14", deadline=date(2024, 1, 1), status="not in progress", parent_id=11,   worker_id=5),
    TaskCreate(name="task_15", deadline=date(2024, 1, 1), status="not in progress", parent_id=None, worker_id=1),
    TaskCreate(name="task_16", deadline=date(2024, 1, 1), status="not in progress", parent_id=6,    worker_id=2),
    TaskCreate(name="task_17", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=3),
    TaskCreate(name="task_18", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=5),
    TaskCreate(name="task_19", deadline=date(2024, 1, 1), status="not in progress", parent_id=None, worker_id=5),
    TaskCreate(name="task_20", deadline=date(2024, 1, 1), status="not in progress", parent_id=None, worker_id=5),
    TaskCreate(name="task_21", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=5),
    TaskCreate(name="task_22", deadline=date(2024, 1, 1), status="done",            parent_id=None, worker_id=5),
    TaskCreate(name="task_23", deadline=date(2024, 1, 1), status="done",            parent_id=None, worker_id=5),
    TaskCreate(name="task_24", deadline=date(2024, 1, 1), status="done",            parent_id=None, worker_id=5),
    TaskCreate(name="task_25", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=4),
    TaskCreate(name="task_26", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=4),
    TaskCreate(name="task_27", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=3),
    TaskCreate(name="task_28", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=4),
    TaskCreate(name="task_29", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=4),
    TaskCreate(name="task_30", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=4),
    TaskCreate(name="task_31", deadline=date(2024, 1, 1), status="in progress",     parent_id=None, worker_id=5),
]


async def init_db(db: AsyncSession = Depends(database.scoped_db_dependency)) -> None:
    for worker in workers:
        await create_worker(db=db, worker_create=worker)

    for task in tasks:
        await create_task(db=db, task_create=task)
