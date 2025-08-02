from app.data.database import Base
from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey

# Entity stored in database
class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())

class CandidateAttempt(Base):
    __tablename__ = "candidate_attempts"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    assessment_id = Column(Integer, ForeignKey("assessments.id")) # referenced from the primary DB
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    evaluated_at = Column(DateTime)
    status = Column(String, default="invited")
    language_choice = Column(String)
    github_repository_link = Column(String)