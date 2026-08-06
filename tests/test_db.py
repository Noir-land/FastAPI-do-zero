from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username="test", email="teste@example.com", password="secret")
        session.add(new_user)
        session.commit()
        user = session.scalar(select(User).where(User.username == "test"))

    assert asdict(user) == {
        "id": 1,
        "username": "test",
        "email": "teste@example.com",
        "password": "secret",
        "created_at": time,
        "update_at": time,
    }


def test_get_session():
    response = get_session()
    session = next(response)

    assert isinstance(session, Session)

    response.close()
