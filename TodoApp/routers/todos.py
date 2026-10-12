from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field

try:
    from ..database import SessionLocal
    from ..models import Todo
    from .auth import get_current_user
except ImportError:
    from database import SessionLocal
    from models import Todo
    from auth import get_current_user

router = APIRouter(tags=["Todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)


@router.get("/")
async def read_all(db: db_dependency):
    return db.query(Todo).all()


@router.get("/todo", status_code=200)
async def get_all_todo_by_user(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_id = user.get("id")
    all_todo = db.query(Todo).filter(Todo.owner_id == user_id).all()
    return all_todo


@router.get("/todo/{todo_id}", status_code=200)
async def read_to_by_id(db: db_dependency, todo_id: int):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo Doesn't Exist")


@router.post("/todo", status_code=201)
async def create_todo(todo: TodoRequest, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    new_todo = Todo(**todo.model_dump(), owner_id=user.get("id"))
    db.add(new_todo)
    db.commit()
    return new_todo


@router.put("/todo/{todo_id}", status_code=204)
async def update_todo(
    todo_id: int,
    todo: TodoRequest,
    db: db_dependency,
    user: user_dependency,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .filter(Todo.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.commit()
    db.refresh(todo_model)

    return todo_model


@router.delete("/todo/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int,
    db: db_dependency,
    user: user_dependency,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .filter(Todo.owner_id == user.get("id"))
        .first()
    )
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
