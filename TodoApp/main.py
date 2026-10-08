from fastapi import FastAPI, Depends, HTTPException
from database import engine, Base, SessionLocal
from typing import Annotated
from models import Todo

from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: str = Field(gt=0, lt=6)
    complete: bool = Field(default=False)


@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todo).all()


@app.get("/todo/{todo_id}", status_code=200)
async def read_to_by_id(db: db_dependency, todo_id: int):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo Doesn't Exist")


@app.post('/todo', status_code=201)
async def create_todo(todo: TodoRequest, db: db_dependency):
    new_todo = Todo(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
