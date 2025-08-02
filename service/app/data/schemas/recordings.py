from app.data.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

class Recording(Base):
    __tablename__ = "recordings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    filename = Column(String, index=True)
    fileSize = Column(Integer, index=True)
    duration = Column(Integer, index=True)
    format = Column(String, index=True)
    createdAt = Column(DateTime, default=func.now())
    hasAudio = Column(Boolean, index=True)
    thumbnailUrl = Column(String, index=True)
