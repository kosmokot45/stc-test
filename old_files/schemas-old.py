from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class TaskBase(BaseModel):
    name: str
    deadline: datetime
    status: str


class TaskCreate(TaskBase):
    ...


class TaskDelete(TaskBase):
    ...


class TaskUpdate(TaskBase):
    name: str
    deadline: datetime
    status: str
    parent_id: Optional[int] = None
    worker_id: Optional[int] = None


class Task(TaskBase):
    id: int
    parent_id: Optional[int] = None
    worker_id: Optional[int] = None

    class Config:
        orm_mode = True


class WorkerBase(BaseModel):
    name: str
    role: str


class WorkerCreate(WorkerBase):
    ...


class WorkerDelete(WorkerBase):
    ...


class Worker(WorkerBase):
    id: int
    # tasks: Optional[list[Task]] = []

    class Config:
        orm_mode = True


class WorkersBusy(BaseModel):
    workers: List[Worker] = []
