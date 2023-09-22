# from fastapi import APIRouter
# # from fastapi import HTTPException
# # from fastapi import status
# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from sqlalchemy.engine import Result

# from core.models import database
# from core.models import Worker  # , WorkerFull
# from workers.schemas import WorkerBusy


# router = APIRouter(tags=["Busy"])


# @router.get("/", response_model=list[WorkerBusy])
# # @router.get("/")
# # -> list[Worker]:
# async def get_busy_workers(db: AsyncSession = Depends(database.scoped_db_dependency)) -> list[Worker]:
#     query = select(Worker)  # .filter(Worker.tasks.status == "in progress")
#     results: Result = await db.execute(query)

#     workers = results.scalars().all()

#     # await asyncio.sleep(0.5)
#     # print("*****************")
#     # for worker in workers:
#     #     print(f"{worker.name, worker.tasks}")
#     # # print("*****************")
#     # return worker.tasks for worker in workers
#     # workers_full = [[result, result.tasks] for result in results]

#     # return workers_full
#     return list(workers)
