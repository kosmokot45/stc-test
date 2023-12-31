from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import date


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
