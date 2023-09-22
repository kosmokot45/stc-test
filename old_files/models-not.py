from datetime import datetime
from sqlalchemy import (
    MetaData,
    TIMESTAMP,
    String,
    Integer,
    Column,
    # Table,
    ForeignKey
)
# from sqlalchemy.orm import relationship
from old_files.db import Base

# from typing import List


metadata = MetaData()


class Worker(Base):
    __tablename__ = "worker"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # tasks = relationship("Task", back_populates="worker")


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    deadline = Column(TIMESTAMP)
    status = Column(String, nullable=False)

    parent_id = Column(Integer, ForeignKey("task.id"))
    worker_id = Column(Integer, ForeignKey("worker.id"))


class BusyWorkers():
    worker_id: int
    task_id: int
    task_name: str
    deadline: datetime
    status: str
    parent_id: int
    # worker_id: int

    # worker = relationship("Worker", back_populates="task")

# worker = Table(
#     "worker",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("role", String, nullable=False),
# )

# task = Table(
#     "task",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("name", String, nullable=False),
#     Column("parent_id", Integer),
#     Column("worker_id", Integer, ForeignKey("worker.id")),
#     Column("deadline", TIMESTAMP),
#     Column("status", String, nullable=False),
# )
