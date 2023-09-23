from typing import Iterable
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .schemas import WorkerCreate, WorkerUpdate
from core.models import Worker


async def get_workers(db: AsyncSession) -> list[Worker]:
    query = select(Worker)
    result: Result = await db.execute(query)
    workers = result.scalars().all()
    return list(workers)


async def get_workers_with_tasks(db: AsyncSession):
    query = select(Worker).options(selectinload(Worker.tasks))
    workers: Iterable[Worker] = await db.scalars(query)
    worker_full: list[Worker] = [
        jsonable_encoder(worker) for worker in workers]

    orderw: list[int] = [len(worker["tasks"])  # type: ignore
                         for worker in worker_full]
    orderw.sort(reverse=True)

    new_b, new_worker_full = zip(
        *[(b, a) for b, a in sorted(zip(orderw, worker_full))])

    return JSONResponse(content=new_worker_full)


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
