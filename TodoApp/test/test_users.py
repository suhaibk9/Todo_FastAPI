from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    res = client.get("/user")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()['username'] == test_user.username
    assert res.json()['email'] == test_user.email
    assert res.json()['first_name'] == test_user.first_name
    assert res.json()['last_name'] == test_user.last_name
    assert res.json()['role'] == test_user.role
    assert res.json()['phone_number'] == test_user.phone_number


def test_password_change(test_user):
    res = client.put('user/password', json={"password": "testpassword", "new_password": "new_password"})
    assert res.status_code == 204


def test_change_password_invalid(test_user):
    res = client.put('user/password', json={"password": "testpassword1", "new_password": "new_password"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Error on password change"}


def test_phone_change(test_user):
    res = client.put("user/phonenumber/123")
    assert res.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    user_model = db.query(Users).filter(Users.id == 1).first()
    assert user_model.phone_number == "123"
