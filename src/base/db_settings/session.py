from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.db_settings.db_helper import db_helper

ISession = Annotated[AsyncSession, Depends(db_helper.get_session)]