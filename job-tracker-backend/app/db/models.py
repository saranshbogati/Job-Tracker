from sqlalchemy import Column, Integer, String, Date
from .session import Base


class Job(Base):
    __tablename__ = "job"
    
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    title = Column(String, index=True)
    date_applied = Column(Date, index=True)
    status = Column(String, index=True)
    description = Column(String, nullable=True)
    