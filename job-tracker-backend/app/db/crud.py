from sqlalchemy.orm import Session
from datetime import datetime
from app.db.models import Job


def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Job).offset(skip).limit(limit).all()


def create_job(
    db: Session,
    company: str,
    date_applied: str,
    status: str,
    title: str,
    description: str = "",
):
    # print("#############################date applied is ", date_applied)
    date_obj = datetime.strptime(date_applied, "%m/%d/%Y").date()
    db_job = Job(
        company=company,
        date_applied=date_obj,
        status=status,
        title=title,
        description=description,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(
    db: Session,
    job_id: int,
    company: str,
    date_applied: str,
    status: str,
    title: str,
    description: str,
):
    job: Job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        return None
    job.company = company
    job.date_applied = date_applied
    job.status = status
    job.title = title
    job.description = description
    db.commit()
    db.refresh(job)
    return job


def delete_job(db: Session, job_id: int):
    db_job: Job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        return None
    db.delete(db_job)
    db.commit()
    return True
