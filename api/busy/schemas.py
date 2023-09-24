from pydantic import BaseModel
from datetime import date
from api.tasks.schemas import Task


class LastEndpoint(BaseModel):
    task: Task
    deadline: date
    name: str
