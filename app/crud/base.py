from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.base_class import Base
from sqlalchemy import or_, and_, Column
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import InstrumentedAttribute,joinedload
from app.core.logging import logger


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):


    def __init__(self, model: Type[ModelType], use_logical_delete: bool = False):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        * `use_logical_delete`: Determines if the model uses logical deletion
        """
        self.model = model
        self._with_deleted = False
        self.use_logical_delete = use_logical_delete

    async def with_deleted(self):
        """Allow fetching records even if they are marked as deleted."""
        # session.query(User).with_deleted().get(1)
        self._with_deleted = True
        return self

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        query = select(self.model).filter(self.model.id == id)

        if not self._with_deleted:
            query = query.filter(self.model.isDeleted == False)

        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_all(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        if not self._with_deleted:
            result = await db.execute(select(self.model).filter(self.model.isDeleted == False).offset(skip).limit(limit))
        else:
            result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def search(
        self, 
        db: AsyncSession, 
        filters: Dict[str, Tuple[Any, str]],
        skip: int = 0, 
        limit: int = 100,
        single_result: bool = False,
        combine_with: str = "and",
        relations: List[ModelType] = [],
    ) -> Union[ModelType, List[ModelType]]:
        # example 
        # filters = {
        #     "name": ("John", "ilike"),
        #     "age": (25, ">"),
        # }
        #await crud_model.search(db, filters=filters, single_result=True, combine_with="or", relations=[Organization.users])
        query = select(self.model)
        
        filter_clauses = []
        for field, (value, filter_type) in filters.items():
            column = getattr(self.model, field, None)

            if not isinstance(column, InstrumentedAttribute):
                raise ValueError(f"Field {field} does not exist in the model.")
            
            if filter_type == "like":
                filter_clauses.append(column.like(f"%{value}%"))
            elif filter_type == "ilike":
                filter_clauses.append(column.ilike(f"%{value}%"))
            elif filter_type == "in":
                if isinstance(value, list):
                    filter_clauses.append(column.in_(value))
                else:
                    raise ValueError(f"Filter type 'in' requires a list of values.")
            elif filter_type == "=":
                filter_clauses.append(column == value)
            elif filter_type == ">":
                filter_clauses.append(column > value)
            elif filter_type == "<":
                filter_clauses.append(column < value)
            elif filter_type == "!=":
                filter_clauses.append(column != value)
            elif filter_type == "is_null":
                if value:
                    filter_clauses.append(column.is_(None))
                else:
                    filter_clauses.append(column.is_not(None))
            else:
                raise ValueError(f"Unsupported filter type {filter_type}")
        
        if combine_with == "or":
            query = query.filter(or_(*filter_clauses))
        else:
            query = query.filter(and_(*filter_clauses))

        if not self._with_deleted:
            query = query.filter(self.model.isDeleted == False)
        
        if relations:
             query = query.options(*[joinedload(relation) for relation in relations])

        if single_result:
            result = await db.execute(query.limit(1))
            return result.scalars().first()
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        obj = result.scalars().first()

        if not obj:
            return None

        if self.use_logical_delete:
            if obj.isDeleted:
                return None
            obj.isDeleted = True
            db.add(obj)
        else:
            await db.delete(obj)

        await db.commit()
        return obj
