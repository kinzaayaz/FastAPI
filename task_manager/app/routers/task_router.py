from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from app.models.task_model import Task, TaskUpdate
from app.db.database import collection_name
from bson import ObjectId
import json

router = APIRouter(prefix = '/tasks',tags=["Tasks"])

@router.get("/about")
def about():
    return {"info": "A fully functional API to manage your tasks"}

@router.get("/view")
def view():
    tasks = list(collection_name.find())
    for task in tasks:
        task["_id"] = str(task['_id'])
    return tasks

@router.get("/view/{task_id}")
def view_task(task_id: str):
    task = collection_name.find_one({"_id":ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task['_id'] = str(task['_id'])
    return task

@router.post("/create")
def create_task(task: Task):
    new_task = task.model_dump()
    result = collection_name.insert_one(new_task)
    return {"message": "task created successfully", "id": str(result.inserted_id)}

@router.put("/update/{task_id}")
def update_task(task_id: str, update_task: TaskUpdate):

    data = update_task.model_dump()
    updated_task={}
    for key,value in data.items():
        if value is not None:
            updated_task[key] = value
    result = collection_name.update_one({"_id":ObjectId(task_id)}, {"$set":updated_task})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Id not found")
    return JSONResponse(status_code=200, content={"message": "updated successfully!"})

@router.delete("/delete/{task_id}")
def delete_task(task_id: str):
    result = collection_name.delete_one({"_id":ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="id not found")
    return JSONResponse(status_code=200, content={"message": "task deleted successfully"})
