from src.base.base_models.dto_models import BaseDto
from src.base_crud.base_repository import BaseRepository, BaseRepositoryPaginate, FileDefaultRepository
from fastapi import UploadFile


class BaseService:
    def __init__(self, repository: BaseRepository | BaseRepositoryPaginate):
        self.repository = repository

    async def create(self, session, model: BaseDto = None):
        result, _ = await self.repository.create(session, model)
        return result

    async def get(self, session, pk: int):
        return await self.repository.get(session, pk)

    async def get_all(self, session, filters):
        stmt = await self.repository.get_all(session, filters)
        return stmt

    async def update(self, session, pk: int, dto: BaseDto):
        return await self.repository.update(session=session, dto=dto, pk=pk)

    async def partial_update(self, session, pk: int, dto: BaseDto):
        return await self.repository.partial_update(session=session, dto=dto, pk=pk)

    async def delete(self, session, pk: int):
        return await self.repository.delete(session, pk)


class GenericService:
    def __init__(self, model, service=BaseService, repository=BaseRepository) -> None:
        self.model = model

        class Repository(repository):
            model = self.model

        self.repository = Repository()
        self.service = service(repository=self.repository)

    def get_service(self):
        return self.service


class GenericServicePaginate:
    def __init__(self, model, service=BaseService, repository=BaseRepositoryPaginate) -> None:
        self.model = model

        class Repository(repository):
            model = self.model

        self.repository = Repository()
        self.service = service(repository=self.repository)

    def get_service(self):
        return self.service


class FileBaseService:
    def __init__(self, repository: FileDefaultRepository):
        self.repository = repository

    async def create(self, session, id: int, file: UploadFile):
        result = await self.repository.create(session, id, file)
        return result

    async def get(self, session, pk: int):
        return await self.repository.get(session, pk)

    async def get_all(self, session, filters):
        stmt = await self.repository.get_all(session, filters)
        return stmt

    async def delete(self, session, pk: int):
        return await self.repository.delete(session, pk)


class FileGenericService:
    def __init__(self, model, field_name, service=FileBaseService, repository=FileDefaultRepository) -> None:
        self.model = model
        self.field_name = field_name

        class Repository(repository):
            model = self.model
            field_name = self.field_name

        self.repository = Repository()
        self.service = service(repository=self.repository)

    def get_service(self):
        return self.service
