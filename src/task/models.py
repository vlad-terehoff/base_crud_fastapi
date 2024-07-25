from src.base.base_models.db_models import Base, str_256
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, false
from sqlalchemy_file.types import FileField
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager


task_files_container = LocalStorageDriver("./src/mediafile").get_container("task_file")
StorageManager.add_storage("task_file", task_files_container)


class FileTaskModel(Base):
    __tablename__ = "task_file"

    file = Column(FileField(upload_storage="task_file"))

    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    task: Mapped["TaskModel"] = relationship(back_populates='file')

    def __repr__(self):
        return f"{self.__class__.__name__}"


class TaskModel(Base):
    __tablename__ = "task"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(back_populates='tasks')

    description: Mapped[str_256]

    is_active: Mapped[bool] = mapped_column(server_default=false())
    file: Mapped[list["FileTaskModel"]] = relationship(back_populates='task')

    def __repr__(self):
        return f"{self.__class__.__name__}"


from src.user.models import UserModel
