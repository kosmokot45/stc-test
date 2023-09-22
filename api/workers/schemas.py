from pydantic import BaseModel, ConfigDict


class WorkerBase(BaseModel):
    name: str
    role: str


class WorkerCreate(WorkerBase):
    ...


class WorkerUpdate(WorkerCreate):
    ...


class Worker(WorkerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
