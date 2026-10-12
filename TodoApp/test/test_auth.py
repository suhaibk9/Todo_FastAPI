from jose.constants import ALGORITHMS

from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, get_current_user, secret, algo
from fastapi import status, HTTPException
from jose import jwt
from datetime import timedelta
import pytest
from datetime import timedelta, datetime, timezone

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    non_existent_user = authenticate_user("incorrect_username", "incorrect_password", db)
    assert non_existent_user is False
    wrong_password_user = authenticate_user(test_user.username, "wrong_password", db)
    assert wrong_password_user is False


# username: str, user_id: int, role: str, expires_delta: timedelta
def test_create_access_token(test_user):
    encode = {
        "username": test_user.username,
        "user_id": test_user.id,
        "role": test_user.role,
        "expires_delta": timedelta(minutes=20),
    }
    token = create_access_token(**encode)
    decoded_token = jwt.decode(token, secret, algorithms=[algo], options={"verify_signature": False})

    assert decoded_token["sub"] == test_user.username
    assert decoded_token["id"] == test_user.id
    assert decoded_token["role"] == test_user.role


@pytest.mark.asyncio
async def test_get_current_valid_token():
    encode = {"sub": "testuser", "id": 1, "role": "admin"}
    token = jwt.encode(encode, secret, algorithm=algo)
    user = await get_current_user(token)
    assert user == {"username": "testuser", "id": 1, "role": "admin"}


@pytest.mark.asyncio
async def test_missing_payload():
    encode = {"id": 1, "role": "admin"}
    token = jwt.encode(encode, secret, algorithm=algo)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Not Allowed"
