# from typing import TYPE_CHECKING
from pydantic import BaseModel, ConfigDict
# from typing import Optional
from datetime import date

# if TYPE_CHECKING:
#     from tasks.schemas import TaskBase


class TaskBase(BaseModel):
    name: str
    deadline: date
    status: str
    parent_id: int | None = None
    worker_id: int | None = None


class WorkerBase(BaseModel):
    name: str
    role: str
    # tasks: Optional[list[TaskBase | None]]


class WorkerCreate(WorkerBase):
    ...


class WorkerUpdate(WorkerCreate):
    ...


class Worker(WorkerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class WorkerBusy(BaseModel):
    tasks: list[TaskBase | None]
