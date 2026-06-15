from datetime import datetime

from pydantic import BaseModel

from app.models.task import Priority


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: Priority = Priority.medium
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: Priority | None = None
    due_date: datetime | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    priority: Priority
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    owner_id: int

    model_config = {"from_attributes": True}
