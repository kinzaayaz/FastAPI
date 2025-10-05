from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from typing import Annotated,Literal,Optional
from fastapi.responses import JSONResponse
import json

app = FastAPI()
tasks = {}

class Task(BaseModel):
    id:Annotated[str, Field(...,description="Id of the task",example="01")]
    title:Annotated[str, Field(...,description="title of the task",example='buy grocery')]
    description:Annotated[str, Field(..., description="description of task",example="milk bread egg")]
    status:Annotated[Literal["Pending","completed"],Field(..., description="Status of the task")]

class TaskUpdate(BaseModel):
    id:Annotated[Optional[str], Field(default=None)]
    title:Annotated[Optional[str], Field(default=None)]
    description:Annotated[Optional[str], Field(default=None)]
    status:Annotated[Optional[Literal["Pending","completed"]], Field(default=None)]

@app.get("/")
def welcome():
    return {"message":"welcome to task manager API"}

@app.get("/about")
def about():
    return {"info":"A fully functional API to manage ur tasks"}

@app.get("/view")
def view():
    return tasks

@app.get("/view/{task_id}")
def view_task(task_id:str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="id not found")
    return tasks[task_id]

@app.post("/create")
def create_task(task:Task):
    if task.id in tasks:
        raise HTTPException(status_code=400, detail="task already exist")
    tasks[task.id]=task
    return {"message":"task created successfully","task":task}

@app.put("/update/{task_id}")
def update_task(task_id:str, update_task:TaskUpdate):
    if task_id not in tasks:
        raise HTTPException (status_code=404, detail="task not found")

    existing_task = tasks[task_id].model_dump()
    updated_data = update_task.model_dump(exclude_unset=True)

    existing_task.update(updated_data)
    tasks[task_id] = Task(**existing_task)
    return JSONResponse(status_code=200, content={"message":"updated successfully!"})


@app.delete("/delete/{task_id}")
def delete_task(task_id:str):
    if task_id not in tasks:
        raise HTTPException(status_code=404,detail="id not found")
    del tasks[task_id]
    return JSONResponse(status_code=200, content={"message":"task deleted successfully"})


