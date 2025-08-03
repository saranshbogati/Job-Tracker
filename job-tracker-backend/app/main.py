from fastapi import FastAPI
from app.db.session import engine
from app.db.models import Base
from app.api import job

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(job.router)


@app.get("/")
def root():
    return {"message": "Job Tracker API"}
