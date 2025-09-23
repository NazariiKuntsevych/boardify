from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    body: Mapped[str] = mapped_column(String(255))
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))
    priority_id: Mapped[int] = mapped_column(ForeignKey("priority.id"))
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id", ondelete="CASCADE"))

    status = relationship("Status", lazy="selectin")
    priority = relationship("Priority", lazy="selectin")
    board = relationship("Board", back_populates="tasks")
