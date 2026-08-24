import os
import sqlite3
from dotenv import load_dotenv
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from auth.auth import router as auth_router
from repository import PostgresTaskRepository

load_dotenv()
app = FastAPI()
repo = PostgresTaskRepository()

app.include_router(auth_router)

@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
async def get_tasks():
    return repo.get_all()

@app.get("/tasks/{task_id}")
async def taskById(task_id: int):
    row = repo.get_by_id(task_id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail={"error": f"Task {task_id} not found"}
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }

@app.post("/tasks", status_code=201)
async def taskPost(title: str):
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail={"error": "Invalid request: title is required"})

    return repo.create(title)

@app.put("/tasks/{task_id}")
async def updateTask(task_id: int, title: Optional[str] = None, done: Optional[bool] = None):
    success = repo.update(task_id,title,done)

    if not success:
        raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})

    return row

@app.delete("/tasks/{task_id}")
async def deleteTask(task_id: int):
    row = repo.delete(task_id)

    if row is None:
        raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})

    return {"message": f"Task {task_id} deleted successfully"}

@app.get("/public/info")
def publicInfo():
    return JSONResponse(
        status_code=200,
        content={
            "message": "Welcome stranger! This info is public."
        }
    )

