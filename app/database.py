from typing import Annotated

from fastapi import Depends
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

DATABASE_URL = settings.DATABASE_URL
DATABASE_PARAMS = {} if settings.ENV == 'local' else {"poolclass": NullPool}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]
