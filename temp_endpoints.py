from fastapi import HTTPException
from typing import Optional

# You can copy and paste these into your main.py when you are ready.

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, title: Optional[str] = None, done: Optional[bool] = None):
    # Iterate through tasks to find the matching ID
    for task in tasks:
        if task["id"] == task_id:
            # Update the title if a new one was provided
            if title is not None:
                if len(title) == 0:
                    raise HTTPException(status_code=400, detail={"Bad request": "Title must not be empty"})
                task["title"] = title
            
            # Update the done status if a new one was provided
            if done is not None:
                task["done"] = done
                
            return task
            
    # If the loop finishes without returning, the task wasn't found
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    for i in range(len(tasks)):
        if tasks[i]["id"] == task_id:
            # Remove the task from the list at index i
            tasks.pop(i)
            # A 204 status code (No Content) doesn't require a return body
            return
            
    # If the loop finishes without returning, the task wasn't found
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})
