# Task Management API
A RESTful API for managing tasks, built with FastAPI and SQLite.

## Setup
```bash
git clone https://github.com/thomsas/task-management-api.git
cd task-management-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
