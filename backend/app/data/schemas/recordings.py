from app.data.database import Base
from sqlmodel import Field
from datetime import datetime

class Recording(Base):
    __tablename__ = "recordings"
    id: int = Field(primary_key=True)
    title: str = Field(index=True)
    filename: str = Field(index=True)
    fileSize: int = Field(index=True)
    duration: int = Field(index=True)
    format: str = Field(index=True) # e.g. "mp4", "webm"
    createdAt: datetime = Field(index=True)
    hasAudio: bool = Field(index=True)
    thumbnailUrl: str | None = Field(index=True)
