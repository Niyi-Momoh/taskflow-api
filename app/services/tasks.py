from sqlalchemy.orm import Session

from app.models.task import Priority, Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(
    db: Session,
    owner_id: int,
    completed: bool | None = None,
    priority: Priority | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[Task]:
    query = db.query(Task).filter(Task.owner_id == owner_id)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    if priority is not None:
        query = query.filter(Task.priority == priority)
    return query.offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int, owner_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()


def create_task(db: Session, data: TaskCreate, owner_id: int) -> Task:
    task = Task(**data.model_dump(), owner_id=owner_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, data: TaskUpdate) -> Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
