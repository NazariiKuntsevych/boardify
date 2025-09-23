from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
