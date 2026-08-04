from http import HTTPStatus

from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):

    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


def test_ola_mundo(client):

    response = client.get("/ola-mundo")
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):

    response = client.post(
        "/users/",
        json={
            "id": 1,
            "username": "Girino",
            "email": "girino@example.com",
            "password": "123456",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "Girino",
        "email": "girino@example.com",
    }


def test_create_username_integrity_error(client):
    client.post(
        "/users/",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )
    response = client.post(
        "/users/",
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_create_email_integrity_error(client):
    client.post(
        "/users/",
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "secret",
        },
    )
    response = client.post(
        "/users/",
        json={
            "username": "grilo",
            "email": "bob@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists"}


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user_ok(client, user, token):
    response = client.put(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "123456",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_update_user_return_not_found(client, user, token):
    response = client.put(
        "/users/-666",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "123456",
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}


def test_delete_user_ok(client, user, token):
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_return_not_found(client, user, token):
    response = client.delete("/users/-2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}


def test_get_user_ok(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_user_error(client, user):
    response = client.get("/users/-1")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_integrity_error(client, user, token):
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )
    response_update = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "secret",
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT.value
    assert response_update.json() == {"detail": "Username or Email already exists"}


def test_get_session():
    response = get_session()
    session = next(response)

    assert isinstance(session, Session)

    response.close()


def test_get_token(client, user):
    response = client.post(
        "/token", data={"username": user.email, "password": user.clean_password}
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_get_token_user_not_found(client, user):

    response = client.post(
        "/token", data={"username": user.username, "password": user.clean_password}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


def test_get_token_password_invadlide(client, user):
    response = client.post(
        "/token", data={"username": user.email, "password": "senha_errada_aqui"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}
