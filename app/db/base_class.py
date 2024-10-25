from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import TIMESTAMP, Column,Boolean
from sqlalchemy.sql import func


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically

    isDeleted = Column(Boolean, default=False, nullable=False, index=True)
    createdAt = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updatedAt = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()