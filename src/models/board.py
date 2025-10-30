from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Board(Base):
    __tablename__ = "board"
    __table_args__ = (
        UniqueConstraint("name", "user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="boards")
    tasks = relationship("Task", back_populates="board", passive_deletes=True)
