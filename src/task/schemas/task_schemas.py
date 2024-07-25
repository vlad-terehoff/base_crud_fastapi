from pydantic import Field
from src.base.base_models.dto_models import BaseDto
from datetime import datetime


class TaskBaseDTO(BaseDto):
    description: str = Field(max_length=256)
    is_active: bool = Field(default=False)


class CreateTaskDTO(TaskBaseDTO):
    user_id: int


class GetTaskDTO(TaskBaseDTO):
    id: int
    user_id: int


class UpdateToolsDTO(CreateTaskDTO):
    pass


class PatchTaskDTO(BaseDto):
    user_id: int | None = Field(default=None)
    description: str | None = Field(max_length=256, default=None)
    is_active: bool | None = Field(default=False)


class GetUserTasksDTO(TaskBaseDTO):
    id: int



class FileToolsFilterDTO(BaseDto):
    tools_id: int


class FileDTO(BaseDto):
    id: int
    created_at: datetime
