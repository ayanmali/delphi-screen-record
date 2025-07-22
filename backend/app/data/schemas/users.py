from app.data.database import Base
from sqlalchemy import Column, DateTime, Integer, String, func

# Entity stored in database
class UserDBModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())