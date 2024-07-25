from collections import defaultdict
from src.base.base_models.dto_models import BaseDto
from src.base_crud.base_controller import ControllerMixin, Controller
from src.user.schemas.user_schemas import CreateUserDTO, PatchUserDTO, ChangeUserRoleDTO
from src.user.service import user_service
from sqlalchemy.ext.asyncio import AsyncSession


class UserController(ControllerMixin, Controller):
    pydantic_model = defaultdict(lambda: CreateUserDTO, {"partial_update": PatchUserDTO,
                                                         "change_role": ChangeUserRoleDTO})
    service = user_service
    slug_field_type = int

    async def get_user_with_tasks(self, session: AsyncSession, pk: int):
        return await self.service.get_user_with_tasks(session, pk)

    async def change_role(self, session: AsyncSession, pk: int,  dto: BaseDto):
        return await self.service.change_role(session, pk,  dto)