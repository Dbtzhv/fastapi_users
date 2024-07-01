from fastapi import HTTPException
from starlette import status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import InstanceNotFound


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, db: Session, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, db: Session, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, db: Session, model_id: int):
        query = select(cls.model).filter_by(id=model_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def add(cls, db: Session, **data):
        query = insert(cls.model).values(**data)
        await db.execute(query)
        await db.commit()
        return f"{cls.model.__name__} has been created"

    @classmethod
    async def update(cls, db: Session, model_id: int, **data):
        query = update(cls.model).where(cls.model.id == model_id).values(**data)
        result = await db.execute(query)
        if result.rowcount == 0:
            await db.rollback()
            raise InstanceNotFound(
                detail=f"{cls.model.__name__} with id {model_id} not found"
            )
        await db.commit()
        return f"{cls.model.__name__} with id {model_id} has been updated"

    @classmethod
    async def delete_by_id(cls, db: Session, model_id: int):
        instance = await cls.find_by_id(db, model_id)
        if instance:
            query = delete(cls.model).filter_by(id=model_id)
            await db.execute(query)
            await db.commit()
            return f"{cls.model.__name__} with id {model_id} has been deleted"
        return instance
