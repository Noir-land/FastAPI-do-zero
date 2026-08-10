from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username="test", email="teste@example.com", password="secret")
        session.add(new_user)
        await session.commit()
    user = await session.scalar(select(User).where(User.username == "test"))

    assert asdict(user) == {
        "id": 1,
        "username": "test",
        "email": "teste@example.com",
        "password": "secret",
        "created_at": time,
        "update_at": time,
    }


@pytest.mark.asyncio
async def test_get_session():
    response = get_session()
    session = await anext(response)

    assert isinstance(session, AsyncSession)

    await response.aclose()
