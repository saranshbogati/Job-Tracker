from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.schema.job import JobCreate, JobOut, JobUpdate
from sqlalchemy.orm import Session
from app.db import crud, session


router = APIRouter(prefix="/job", tags=["Jobs"])


def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=JobOut)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(
        db,
        company=job.company,
        date_applied=job.date_applied.strftime("%m/%d/%Y"),
        status=job.status,
        title=job.title,
        description=job.description,
    )


@router.get("", response_model=List[JobOut])
def get_all_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_jobs(db, skip=skip, limit=limit)


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobOut)
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    updated = crud.update_job(
        db,
        job_id,
        company=job.company,
        date_applied=job.date_applied.strftime("%Y-%m-%d"),
        status=job.status,
        title=job.title,
        description=job.description,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Job not found")
    return updated


@router.delete("/{job_id}", response_model=dict)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    success = crud.delete_job(db, job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}
