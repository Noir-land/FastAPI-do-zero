from http import HTTPStatus

from fast_zero.schemas import UserPublic


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


def test_create_username_integrity_error(client, user):
    client.post(
        "/users/",
        json={
            "username": user.username,
            "email": "fausto@example.com",
            "password": "secret",
        },
    )
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "email": "bob@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_create_email_integrity_error(client, user):
    client.post(
        "/users/",
        json={
            "username": "fausto",
            "email": user.email,
            "password": "secret",
        },
    )
    response = client.post(
        "/users/",
        json={
            "username": "grilo",
            "email": user.email,
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
        f"/users/{user.id}",
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
        f"/users/{user.id - 1}",
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
    response = client.delete(
        f"/users/{user.id - 2}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}


def test_get_user_ok(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(f"/users/{user.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_user_error(client, user):
    response = client.get(f"/users/{user.id - 1}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_integrity_error(client, user, other_user, token):
    response_update = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": other_user.username,
            "email": "bob@example.com",
            "password": "secret",
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT.value
    assert response_update.json() == {"detail": "Username or Email already exists"}


def test_update_user_with_wrong_user(client, user, token):
    response = client.put(
        f"/users/{user.id + 1}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}


def test_update_user_with_wrong_other_user(client, other_user, token):
    response = client.put(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}
