from pydantic import BaseModel,Field
from typing import Annotated,Literal,Optional

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