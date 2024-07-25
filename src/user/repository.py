from src.base.base_models.dto_models import BaseDto
from src.base_crud.base_repository import BaseRepository
from src.user.models import UserModel
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload


class UserRepository(BaseRepository):
    model = UserModel

    async def get_user_with_tasks(self, session, pk: int):
        stmt = select(self.model).options(selectinload(self.model.tasks)).where(self.model.id == pk)
        raw = await session.execute(stmt)
        return raw.scalar_one()

    async def change_role(self, session, pk: int,  dto: BaseDto):
        stmt = update(self.model).values(dto.model_dump()).filter_by(id=pk).returning(self.model)
        raw = await session.execute(stmt)
        await session.commit()
        return raw.scalar_one()


user_repository = UserRepository()
