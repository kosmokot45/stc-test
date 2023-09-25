from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from datetime import date

from .base import Base


if TYPE_CHECKING:
    from .worker import Worker


class Task(Base):
    name: Mapped[str]
    deadline: Mapped[date]
    status: Mapped[str]
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"))
    child: Mapped["Task"] = relationship("Task", lazy="joined", join_depth=2)

    # worker_id: Mapped[int | None] = mapped_column(ForeignKey("workers.id"))
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    worker: Mapped["Worker"] = relationship(back_populates="tasks")
