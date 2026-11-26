from enum import Enum

from pydantic import BaseModel, Field


class TaskState(str, Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1,max_length=100)
    state: TaskState = TaskState.TODO

class TasksUpdate(BaseModel):
    title: str | None= Field(min_length=1, max_length=20, default=None)
    description: str | None= Field(min_length=1, max_length=100,default=None)
    state: TaskState

class TasksOut(BaseModel):
    id: int
    title: str
    description: str
    state: TaskState