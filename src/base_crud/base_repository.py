from sqlalchemy.exc import NoResultFound
from fastapi import UploadFile
from src.base.base_models.dto_models import BaseDto
from sqlalchemy import select, update, delete
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_filters.ext.sqlalchemy import apply_filters
from sqlalchemy_file.types import File
from src.exceptions import exec_catch, exec_catch_none


class RepositoryWithoutPaginate:
    async def get_all(self, session, filters):
        stmt = await session.scalars(apply_filters(select(self.model), filters))
        return stmt.all()


class RepositoryWithPaginate:
    async def get_all(self, session, filters):
        stmt = await paginate(session, apply_filters(select(self.model), filters))
        return stmt


class DefaultRepository:
    model = None

    async def create(self, session, obj: BaseDto):
        try:

            stmt = select(self.model).filter_by(**obj.model_dump())
            raw = await session.execute(stmt)
            return raw.scalar_one(), False

        except NoResultFound:

            instance = self.model(**obj.model_dump())
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance, True

    @exec_catch_none
    async def get(self, session, pk: int):
        raw = await session.get(self.model, pk)
        return raw

    async def update(self, pk: int, session, dto: BaseDto):
        stmt = update(self.model).values(**dto.model_dump()).filter_by(id=pk).returning(self.model)
        raw = await session.execute(stmt)
        await session.commit()
        return raw.scalar_one()

    async def partial_update(self, pk: int, session, dto: BaseDto):
        update_data = dto.model_dump(exclude_none=True)
        stmt = update(self.model).values(update_data).filter_by(id=pk).returning(self.model)
        raw = await session.execute(stmt)
        await session.commit()
        return raw.scalar_one()

    async def delete(self, session, pk: int) -> None:
        stmt = delete(self.model).where(self.model.id == pk)
        await session.execute(stmt)
        await session.commit()


class BaseRepositoryPaginate(DefaultRepository, RepositoryWithPaginate):
    pass


class BaseRepository(DefaultRepository, RepositoryWithoutPaginate):
    pass


class FileDefaultRepository:
    model = None
    field_name = None

    async def create(self, session, id: int, file: UploadFile):
        file = File(content=file.file, filename=file.filename, content_type=file.content_type)
        data_dict = {self.field_name: id, "file": file}
        instance = self.model(**data_dict)

        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @exec_catch
    async def get(self, session, pk: int):
        stmt = select(self.model).filter_by(id=pk)
        raw = await session.execute(stmt)
        return raw.scalar_one()

    async def get_all(self, session, filters):
        stmt = await session.scalars(apply_filters(select(self.model), filters))
        return stmt.all()

    async def delete(self, session, pk: int) -> None:
        stmt = delete(self.model).where(self.model.id == pk)
        await session.execute(stmt)
        await session.commit()