from pydantic import Field
from src.base.base_models.dto_models import BaseDto
from typing import List
from src.task.schemas.task_schemas import GetUserTasksDTO
from src.user.models import UserRole


class UserBaseDTO(BaseDto):
    loggin: str = Field(max_length=256)
    first_name: str = Field(max_length=256)
    last_name: str = Field(max_length=256)
    role: UserRole


class CreateUserDTO(UserBaseDTO):
    pass


class GetUserDTO(UserBaseDTO):
    id: int


class GetUserAndTasksDTO(UserBaseDTO):
    id: int
    tasks: List[GetUserTasksDTO]


class UpdateUserDTO(UserBaseDTO):
    pass


class ChangeUserRoleDTO(BaseDto):
    role: UserRole


class PatchUserDTO(UserBaseDTO):
    loggin: str | None = Field(max_length=256, default=None)
    first_name: str | None = Field(max_length=256, default=None)
    last_name: str | None = Field(max_length=256, default=None)

