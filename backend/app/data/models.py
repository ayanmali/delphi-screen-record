from datetime import datetime
from typing import Literal
from sqlmodel import Field, SQLModel

# Schema
class Recording(SQLModel, table=True):
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

# Data Transfer Objects
class InsertRecording(SQLModel, table=False):
    title: str = Field(index=True)
    filename: str = Field(index=True)
    fileSize: int = Field(index=True)
    duration: int = Field(index=True)
    format: str = Field(index=True)
    hasAudio: bool = Field(index=True)
    thumbnailUrl: str | None = Field(index=True)

class ClientMetadata(SQLModel, table=False):
    title: str = Field(index=True)
    filename: str = Field(index=True)
    duration: int = Field(index=True)
    format: str = Field(index=True)
    hasAudio: bool = Field(index=True)
    thumbnailUrl: str | None = Field(index=True)

class RecordingOptions(SQLModel, table=False):
    screenSource: Literal["entire", "window", "tab"] = Field(index=True)
    includeMicrophone: bool = Field(index=True)
    includeSystemAudio: bool = Field(index=True)
    microphoneVolume: int = Field(..., ge=0, le=100, index=True)
    format: Literal["mp4", "webm"] = Field(index=True)