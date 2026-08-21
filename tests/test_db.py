from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import Todo, User


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
        "updated_at": time,
        "todos": [],
    }


@pytest.mark.asyncio
async def test_get_session():
    response = get_session()
    session = await anext(response)

    assert isinstance(session, AsyncSession)

    await response.aclose()


@pytest.mark.asyncio
async def test_create_todo(session, user):
    todo = Todo(
        title="Test todo",
        description="Test Desc",
        state="draft",
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()

    todo = await session.scalar(select(Todo))

    assert asdict(todo) == {
        "description": "Test Desc",
        "id": 1,
        "state": "draft",
        "title": "Test todo",
        "user_id": 1,
        "created_at": todo.created_at,
        "updated_at": todo.updated_at,
    }


@pytest.mark.asyncio
async def test_user_todo_relationship(session, user: User):
    todo = Todo(
        user_id=user.id,
        title="Test Todo",
        description="Test Desc",
        state="draft",
    )

    session.add(todo)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(select(User).where(User.id == user.id))

    assert user.todos == [todo]
