from typing import Annotated
from sqlalchemy import String, text
from datetime import datetime
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# String - ограничивает количество символов для строки

str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    """Базовая модель SqlAlchemy"""
    __abstract__ = True
    type_annotation_map = {
        str_256: String(256)
    }


    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
