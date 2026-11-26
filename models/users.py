from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

# 仅用于 IDE 类型提示，运行时不导入，防止循环引用
if TYPE_CHECKING:
    from .tasks import Task

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255)) # 如果存哈希值，建议改为 String(255)
    email: Mapped[str] = mapped_column(String(120))
    age: Mapped[int | None] = mapped_column(default=None)

    # 核心关联：back_populates 指向 Task 里的关系属性 "owner"
    tasks: Mapped[List["Task"]] = relationship(back_populates="owner")