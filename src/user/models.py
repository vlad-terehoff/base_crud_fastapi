from enum import StrEnum
from src.base.base_models.db_models import Base, str_256
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserRole(StrEnum):
    ADMIN = "Admin"
    USER = "User"


class UserModel(Base):
    __tablename__ = 'user'
    loggin: Mapped[str_256]
    first_name: Mapped[str_256]
    last_name: Mapped[str_256]

    role: Mapped[UserRole]

    tasks: Mapped[list["TaskModel"]] = relationship(back_populates='user')

    def __repr__(self):
        return f"{self.__class__.__name__}"

from src.task.models import TaskModel
