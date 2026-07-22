from fastapi import status
from typing import Optional
from starlette.responses import JSONResponse
from fastapi import HTTPException
from fastapi import FastAPI
import sqlite3

app = FastAPI()

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("select * from tasks")
rows =  cursor.fetchall()
if not rows:
    cursor.executemany(
        "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
        [
            (1, "Learn FastAPI", 0),
            (2, "Build CRUD API", 0),
            (3, "Push project to GitHub", 1),
        ]
    )
    conn.commit()





@app.get("/")
def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    return [
        {"id": row[0], "title": row[1], "done": bool(row[2])}
        for row in rows
    ]

@app.get("/tasks/{task_id}")
async def taskById(task_id: int):
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

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
    cursor.execute("SELECT MAX(id) FROM tasks")
    max_id = cursor.fetchone()[0]
    new_id = 1 if max_id is None else max_id + 1

    cursor.execute(
        "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
        (new_id, title, 0)
    )
    conn.commit()

    return {
        "id" : new_id,
        "title" : title,
        "done" : False
    }

@app.put("/tasks/{task_id}")
async def updateTask(task_id: int, title: Optional[str] = None, done: Optional[bool] = None):
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})

    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (new_title, new_done, task_id)
    )
    conn.commit()


@app.delete("/tasks/{task_id}")
async def deleteTask(task_id: int):
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    if cursor.rowcount == 0:
        raise HTTPException(...)

    conn.commit()
