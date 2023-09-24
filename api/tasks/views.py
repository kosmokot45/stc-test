from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import database
from . import crud
from .schemas import Task, TaskCreate, TaskUpdate

router = APIRouter(tags=["Tasks"])


@router.get("/", response_model=list[Task])
async def get_tasks(db: AsyncSession = Depends(database.scoped_db_dependency)):
    return await crud.get_tasks(db=db)


@router.get("/second/")  # , response_model=list[Task])
async def get_workers_todo(db: AsyncSession = Depends(database.scoped_db_dependency)):
    return await crud.get_workers_todo(db=db)


@router.post("/", response_model=Task)
async def create_task(task_create: TaskCreate, db: AsyncSession = Depends(database.scoped_db_dependency)):
    return await crud.create_task(db=db, task_create=task_create)


@router.get("/{task_id}/", response_model=Task)
async def get_task(task_id: int, db: AsyncSession = Depends(database.scoped_db_dependency)):
    task = await crud.get_task(db=db, task_id=task_id)
    if task is not None:
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    )


@router.put("/{task_id}/", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(database.scoped_db_dependency)):
    task = await crud.get_task(db=db, task_id=task_id)
    if task is not None:
        return await crud.update_task(db=db, task=task, task_update=task_update)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    )


@router.delete("/{task_id}/")
async def delete_task(task_id: int, db: AsyncSession = Depends(database.scoped_db_dependency)) -> None:
    task = await crud.get_task(db=db, task_id=task_id)
    if task is not None:
        return await crud.delete_task(db=db, task=task)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    )
