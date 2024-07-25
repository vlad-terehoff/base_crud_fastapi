from typing import Dict, Type
from src.base.base_models.dto_models import BaseDto
from src.base_crud.base_meta_class import DynamicParamMeta
from src.base_crud.base_service import BaseService
from fastapi_filters import FilterValues
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from sqlalchemy_file.types import File
from starlette.responses import StreamingResponse
from sqlalchemy_file.storage import StorageManager


class Controller(metaclass=DynamicParamMeta):
    pydantic_model: Dict[str, Type[BaseDto]] | None
    service: BaseService
    url_field: str = "pk"


class ControllerMixin:
    async def create(self, session: AsyncSession, model: BaseDto):
        return await self.service.create(session, model)

    async def get(self, session: AsyncSession, pk: int):
        return await self.service.get(session, pk)

    async def get_all(self, session: AsyncSession, filters: FilterValues):
        stmt = await self.service.get_all(session, filters)
        return stmt

    async def update(self, session: AsyncSession, dto: BaseDto, pk: int):
        return await self.service.update(session=session, dto=dto, pk=pk)

    async def partial_update(self, session: AsyncSession, dto: BaseDto, pk: int):
        return await self.service.partial_update(session=session, dto=dto, pk=pk)

    async def delete(self, session: AsyncSession, pk: int):
        return await self.service.delete(session=session, pk=pk)


class FileControllerMixin:
    async def create(self, session: AsyncSession, id: int, file: UploadFile):
        return await self.service.create(session, id, file)

    async def get(self, session: AsyncSession, pk: int):
        file: File = await self.service.get(session, pk)
        file_store = StorageManager.get_file(file.file["path"])
        return StreamingResponse(file_store.object.as_stream(), media_type=file.file["content_type"])

    async def get_all(self, session: AsyncSession, filters: FilterValues):
        stmt = await self.service.get_all(session, filters)
        return stmt

    async def delete(self, session: AsyncSession, pk: int):
        file: File = await self.service.get(session, pk)
        StorageManager.delete_file(file.file["path"])
        return await self.service.delete(session=session, pk=pk)