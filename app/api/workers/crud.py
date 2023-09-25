from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import WorkerCreate, WorkerUpdate
from app.core.models import Worker


async def get_workers(db: AsyncSession) -> list[Worker]:
    query = select(Worker)
    result: Result = await db.execute(query)
    workers = result.scalars().all()
    return list(workers)


async def get_worker(db: AsyncSession, worker_id: int) -> Worker | None:
    return await db.get(Worker, worker_id)


async def create_worker(db: AsyncSession, worker_create: WorkerCreate) -> Worker:
    worker = Worker(**worker_create.model_dump())
    db.add(worker)
    await db.commit()
    return worker


async def update_worker(db: AsyncSession, worker: Worker, worker_update: WorkerUpdate) -> Worker:
    for key, value in worker_update.model_dump().items():
        setattr(worker, key, value)
    await db.commit()
    return worker


async def delete_worker(db: AsyncSession, worker: Worker) -> None:
    await db.delete(worker)
    await db.commit()
