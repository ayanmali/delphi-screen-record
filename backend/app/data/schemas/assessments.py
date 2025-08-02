from pydantic import BaseModel
from app.data.database import Base
from sqlalchemy import Column, DateTime, Integer, String, func, JSON

class AssessmentBase(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    createdAt = Column(DateTime, default=func.now())
