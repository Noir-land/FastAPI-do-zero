from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        "/auth/token", data={"username": user.email, "password": user.clean_password}
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_get_token_user_not_found(client, user):

    response = client.post(
        "/auth/token", data={"username": user.username, "password": user.clean_password}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


def test_get_token_password_invadlide(client, user):
    response = client.post(
        "/auth/token", data={"username": user.email, "password": "senha_errada_aqui"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}
