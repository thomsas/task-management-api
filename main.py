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

@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_database)):
    tasks = db.query(Task).all()
    return tasks

@app.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_database)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        return {"error": "Task not found"}
    return task

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_database)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        return {"error": "Task not found"}
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_database)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        return {"error": "Task not found"}
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}