from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from .task import Task

from .base import Base


class Worker(Base):
    name: Mapped[str]
    role: Mapped[str]

    # tasks: Mapped[list[Task]] = relationship("Task", back_populates="worker",lazy="selectin")
    tasks: Mapped[list[Task]] = relationship("Task", back_populates="worker")
    # tasks: Mapped[list[Task]] = relationship("Task", secondary=WorkerFull, back_populates="worker",lazy="selectin")


# class WorkerFull(Base):

#     tasks: Mapped[list[Task]] = relationship(
#         Task, secondary=Worker.__tablename__, lazy="joined")
