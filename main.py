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