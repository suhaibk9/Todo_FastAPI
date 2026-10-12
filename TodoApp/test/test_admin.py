from .utils import *
from ..routers.admin import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all(test_todo):
    res = client.get("/admin/todo")
    assert res.status_code == 200
    assert res.json() == [
        {
            "complete": False,
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "id": 1,
            "priority": 5,
            "owner_id": 1,
        }
    ]


def test_admin_delete(test_todo):
    res = client.delete("/admin/todo/1")
    assert res.status_code == 204
    db = TestingSessionLocal()
    find_todo_1 = db.query(Todo).filter(Todo.id == 1).first()
    assert find_todo_1 is None
