from jwt import decode

from fast_zero.security import ALGORITHM, SECRECT_KEY, create_acess_token


def test_jwt():
    data = {"test": "test"}
    token = create_acess_token(data)
    decoded = decode(token, SECRECT_KEY, algorithms=ALGORITHM)

    assert decoded["test"] == data["test"]
    assert "exp" in decoded
