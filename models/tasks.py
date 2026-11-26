from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.users import User

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(50))

    # 1. 数据库层面的外键
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # 2. ORM 层面的关系对象 (back_populates 指向 User 里的 "tasks")
    owner: Mapped["User"] = relationship(back_populates="tasks")