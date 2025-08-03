from pydantic import BaseModel, field_validator, validator
from typing import Optional
from datetime import date, datetime


class JobBase(BaseModel):
    company: str
    title: str
    status: str
    description: Optional[str] = ""
    date_applied: date

    @field_validator("date_applied", mode="before")
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%m/%d/%y").date()
        except ValueError:
            try:
                return datetime.strptime(value, "%m/%d/%Y").date()
            except ValueError:
                raise ValueError("Date must be in MM/DD/YY or MM/DD/YYYY format")


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    # job_id: int
    pass


class JobOut(JobBase):
    id: int

    class Config:
        orm_mode = True
