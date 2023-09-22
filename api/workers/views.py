from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import database
from . import crud
from .schemas import Worker, WorkerCreate, WorkerUpdate

router = APIRouter(tags=["Workers"])


@router.get("/", response_model=list[Worker])
async def get_workers(db: AsyncSession = Depends(database.scoped_db_dependency)):
    return await crud.get_workers(db=db)


@router.post("/", response_model=Worker)
async def create_worker(worker_create: WorkerCreate, db: AsyncSession = Depends(database.scoped_db_dependency)):
    return await crud.create_worker(db=db, worker_create=worker_create)


@router.get("/{worker_id}/", response_model=Worker)
async def get_worker(worker_id: int, db: AsyncSession = Depends(database.scoped_db_dependency)):
    worker = await crud.get_worker(db=db, worker_id=worker_id)
    if worker is not None:
        return worker
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Worker {worker_id} not found"
    )


@router.put("/{worker_id}/", response_model=Worker)
async def update_worker(worker_id: int, worker_update: WorkerUpdate, db: AsyncSession = Depends(database.scoped_db_dependency)):
    worker = await crud.get_worker(db=db, worker_id=worker_id)
    if worker is not None:
        return await crud.update_worker(db=db, worker=worker, worker_update=worker_update)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Worker {worker_id} not found"
    )


@router.delete("/{worker_id}/")
async def delete_worker(worker_id: int, db: AsyncSession = Depends(database.scoped_db_dependency)) -> None:
    worker = await crud.get_worker(db=db, worker_id=worker_id)
    if worker is not None:
        return await crud.delete_worker(db=db, worker=worker)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Worker {worker_id} not found"
    )
