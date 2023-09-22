from pydantic import BaseModel, ConfigDict
from datetime import date
# from api.workers.schemas import Worker
# from api.tasks.schemas import TaskBase


# class BusyWorker(Worker):
#     tasks: list[TaskBase]


# class Busy(BusyWorker):
#     ...


class TaskBase(BaseModel):
    name: str
    deadline: date
    status: str
    parent_id: int | None = None
    worker_id: int | None = None


class TaskCreate(TaskBase):
    ...


class TaskUpdate(TaskCreate):
    ...


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
