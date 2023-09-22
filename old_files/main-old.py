# import uvicorn
from typing import List

from fastapi import FastAPI, HTTPException, Depends
# from models import metadata
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

import crud
import core.models.models as models
import old_files.schemas as schemas
from old_files.db import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="STC")


@app.post("/workers/", response_model=schemas.Worker)
def create_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    return crud.create_worker(db=db, worker=worker)


@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, worker_id: int, parent_id: int | None = None, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task, worker_id=worker_id, parent_id=parent_id)


@app.get("/workers/", response_model=List[schemas.Worker])
def read_workers(offset: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    return crud.get_workers(db=db, offset=offset, limit=limit)


@app.get("/workers/{worker_id}", response_model=schemas.Worker)
def read_worker(worker_id: int, db: Session = Depends(get_db)):
    db_worker = crud.get_worker(db=db, worker_id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(offset: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    return crud.get_tasks(db, offset=offset, limit=limit)


@app.put("/workers/{worker_id}", response_model=schemas.Worker)
def put_worker(worker_id: int, data: schemas.WorkerCreate, db: Session = Depends(get_db)):
    db_update_worker = crud.update_worker(
        db=db, worker_id=worker_id, data=data)
    return db_update_worker


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def put_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_update_task = crud.update_task(
        db=db, task_id=task_id, data=data)
    return db_update_task


@app.delete("/workers/{worker_id}", response_model=schemas.WorkerDelete)
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    db_delete_worker = crud.delete_worker(db=db, worker_id=worker_id)
    return db_delete_worker


@app.delete("/tasks/{task_id}", response_model=schemas.TaskDelete)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_delete_task = crud.delete_task(db=db, task_id=task_id)
    return db_delete_task


# # @app.get("/workers/busy/", response_model=List[schemas.WorkersBusy])
# @app.get("/workers/busy/")
# def get_busy_workers(db: Session = Depends(get_db)):
#     # db_busy = db.query(schemas.WorkersBusy).order_by()
#     # db_busy_w = db.query(models.Worker)
#     # old
#     # db_busy = db.query(models.Worker).join(models.Task).filter(models.Task.status=='in progress').group_by(models.Worker.id).order_by(desc(func.count(models.Worker.id))).all()
#     # print('----------')
#     # for el in db_busy:
#     #     print(el.__dict__)
#     # print('----------')
#     # return db_busy
#     # new_tst
#     db_cnt = db.query(models.Task.worker_id, func.count(models.Task.id)).filter(models.Task.status=='in progress').group_by(models.Task.worker_id).order_by(func.count(models.Task.id))
#     # subq = db_cnt.subquery()
#     # db_task = db.query(models.Task, subq).filter(models.Task.worker_id==subq.worker_id and models.Task.status=='in progress')
#     return db_cnt


# @app.get("/tasks/important/")
# def get_important_tasks(db: Session = Depends(get_db)):
#     # db_task = db.query(models.Task)
#     """select * from task 
#         join (select parent_id as id from task 
# 	            where status = 'no' and parent_id is not null) q1 on q1.id = task.id
#         where status = 'in progress'"""
#     # db_tasks = db.query(models.Task).join(db.query("tst", models.Task.parent_id).filter(models.Task.status=='no' and models.Task.parent_id is not None)).filter(models.Task.status=='in progress')    
#     ...
    
    
# # if __name__ == '__main__':
# #     uvicorn.run("app", reload=True)