from fastapi import FastAPI, Depends
from database import engine, get_db
from sqlalchemy.orm import Session
from models.task import Task
from pydantic import BaseModel

app = FastAPI()

def get_database():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "pending"

@app.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_database)):
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task