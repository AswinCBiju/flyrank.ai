from fastapi import status
from typing import Optional
from starlette.responses import JSONResponse
from fastapi import HTTPException
from fastapi import FastAPI

app = FastAPI()

tasks = [
    {
        "id": 1,
        "title": "task1",
        "done": False
    },
    {
        "id": 2,
        "title": "task2",
        "done": False
    },
    {
        "id": 3,
        "title": "task3",
        "done": False
    }
]

@app.get("/")
def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
async def taskById(task_id: int):
    for i in range(len(tasks)):
        if tasks[i]["id"] == task_id:
            return tasks[i]
    raise HTTPException(
        status_code=404,
        detail={"error": f"Task {task_id} not found"}
    )


@app.post("/tasks", status_code=201)
async def taskPost(title: str):
    if not title or len(title) == 0:
        raise HTTPException(
            status_code=404,
            detail={"Bad request" : "Title must not be empty"}
        )
    new_task = {
        "id" : tasks[-1]["id"] + 1 if tasks else 1,
        "title" : title,
        "done" : False
    }
    tasks.append(new_task)
    return tasks


@app.put("/tasks/{task_id}")
async def updateTask(task_id: int, title: Optional[str] = None, done: Optional[bool] = None):
    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                if len(title) == 0:
                    raise HTTPException(
                        status_code = 400,
                        detail = {"Bad request": "Title must not be empty"}
                    )
                task["title"] = title
            if done is not None:
                task["done"] = done
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})


@app.delete("/tasks/{task_id}")
async def deleteTask(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return JSONResponse(
                status_code = 204,
                content = {}
            )
    raise HTTPException(
        status_code = 404,
        detail = {"Bad request": f"Task {task_id} not found"}
    )
