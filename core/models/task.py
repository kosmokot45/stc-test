from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import date

from .base import Base


if TYPE_CHECKING:
    from .worker import Worker


class Task(Base):
    name: Mapped[str]
    deadline: Mapped[date]
    status: Mapped[str]
    parent_id: Mapped[int]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))

    worker: Mapped[Worker] = relationship(
        "Worker", back_populates="tasks")