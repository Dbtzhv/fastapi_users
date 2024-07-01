from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db


async def test_get_db():
    db = get_db()
    assert isinstance(db, AsyncGenerator)

    session = await anext(db)
    assert isinstance(session, AsyncSession)

    with pytest.raises(StopAsyncIteration):
        await anext(db)
