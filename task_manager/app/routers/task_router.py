from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from app.models.task_model import Task, TaskUpdate
from app.utils.storage import tasks
import json

router = APIRouter(tags=["Tasks"])

@router.get("/about")
def about():
    return {"info": "A fully functional API to manage your tasks"}

@router.get("/view")
def view():
    return tasks

@router.get("/view/{task_id}")
def view_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="id not found")
    return tasks[task_id]

@router.post("/create")
def create_task(task: Task):
    if task.id in tasks:
        raise HTTPException(status_code=400, detail="task already exists")
    tasks[task.id] = task
    return {"message": "task created successfully", "task": task}

@router.put("/update/{task_id}")
def update_task(task_id: str, update_task: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="task not found")

    existing_task = tasks[task_id].model_dump()
    updated_data = update_task.model_dump(exclude_unset=True)

    existing_task.update(updated_data)
    tasks[task_id] = Task(**existing_task)
    return JSONResponse(status_code=200, content={"message": "updated successfully!"})

@router.delete("/delete/{task_id}")
def delete_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="id not found")
    del tasks[task_id]
    return JSONResponse(status_code=200, content={"message": "task deleted successfully"})
