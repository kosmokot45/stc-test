from sqlalchemy.orm import Session
# from sqlalchemy import update
from fastapi import HTTPException

import core.models.models as models
import old_files.schemas as schemas


def get_worker(db: Session, worker_id: int):
    db_worker = db.query(models.Worker).filter(
        models.Worker.id == worker_id).first()
    return db_worker


def get_workers(db: Session, offset: int = 0, limit: int = 30):
    return db.query(models.Worker).offset(offset).limit(limit).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, offset: int = 0, limit: int = 30):
    return db.query(models.Task).offset(offset).limit(limit).all()


def create_worker(db: Session, worker: schemas.WorkerCreate):
    db_worker = models.Worker(name=worker.name, role=worker.role)
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


def create_task(db: Session, task: schemas.TaskCreate, worker_id: int, parent_id: int | None = None):
    db_task = models.Task(name=task.name, deadline=task.deadline, status=task.status,
                          worker_id=worker_id, parent_id=parent_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_worker(db: Session, worker_id: int, data: schemas.WorkerCreate):
    db_worker = get_worker(db=db, worker_id=worker_id)
    if not db_worker:
        raise HTTPException(
            status_code=404, detail="Worker not found to update")
    db_worker.name = data.name
    db_worker.role = data.role
    db.commit()
    db.refresh(db_worker)

    return db_worker


def update_task(db: Session, task_id: int, data: schemas.TaskUpdate):
    db_task = get_task(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(
            status_code=404, detail="Task not found to update")
    db_task.name = data.name
    db_task.deadline = data.deadline
    db_task.status = data.status
    db_task.worker_id = data.worker_id
    db_task.parent_id = data.parent_id
    db.commit()
    db.refresh(db_task)

    return db_task


def delete_worker(db: Session, worker_id: int):
    db_worker = get_worker(db=db, worker_id=worker_id)
    if not db_worker:
        raise HTTPException(
            status_code=404, detail="Worker not found to update")
    db.delete(db_worker)
    db.commit()
    return db_worker


def delete_task(db: Session, task_id: int):
    db_task = get_task(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(
            status_code=404, detail="Task not found to update")
    db.delete(db_task)
    db.commit()
    return db_task
