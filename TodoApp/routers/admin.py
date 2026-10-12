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

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/todo", status_code=200)
async def allTodo(db: db_dependency, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="auth failed")
    return db.query(Todo).all()

@router.delete('/todo/{todoId}',status_code=204)
async def delete_todo(todoId:int,db:db_dependency,user:user_dependency):
    if user is None or user.get('role')!='admin':
        raise HTTPException(status_code=401,detail="auth failed")
    todo_model=db.query(Todo).filter(Todo.id==todoId).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="todo not found")
    db.delete(todo_model)
    db.commit()