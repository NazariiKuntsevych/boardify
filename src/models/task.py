from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    body: Mapped[str] = mapped_column(String(255))
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id", ondelete="CASCADE"))

    board = relationship("Board", back_populates="tasks")
