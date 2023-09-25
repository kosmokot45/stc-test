from fastapi import APIRouter
# from fastapi import HTTPException
# from fastapi import status
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.models import database
from . import functions
# from api.workers.schemas import WorkerBusy
from .schemas import LastEndpoint

router = APIRouter(tags=["Busy"])


# , response_model_exclude_none=True)
@router.get("/second/", response_model=list[LastEndpoint])
async def get_workers_todo(db: AsyncSession = Depends(database.scoped_db_dependency)):
    return await functions.get_workers_todo(db=db)


@router.get("/workers/")  # , response_model=list[WorkerBusy])
async def get_busy_workers_with_tasks(db: AsyncSession = Depends(database.scoped_db_dependency)):
    return await functions.get_workers_with_tasks(db=db)
