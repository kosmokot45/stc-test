from pydantic import BaseModel
from datetime import date


class LastEndpoint(BaseModel):
    task_id: int
    task_name: str
    deadline: date
    name: str
