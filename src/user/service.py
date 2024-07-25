from src.base.base_models.dto_models import BaseDto
from src.base_crud.base_service import BaseService
from src.user.repository import user_repository


class UserService(BaseService):

    async def get_user_with_tasks(self, session, pk: int):
        return await self.repository.get_user_with_tasks(session, pk)

    async def change_role(self, session, pk: int,  dto: BaseDto):
        return await self.repository.change_role(session, pk,  dto)


user_service = UserService(repository=user_repository)