from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from .task import Task

from .base import Base


class Worker(Base):
    name: Mapped[str]
    role: Mapped[str]

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="worker"
    )
