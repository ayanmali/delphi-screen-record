from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field

class Recording(BaseModel):
    id: int
    title: str
    filename: str
    fileSize: int
    duration: int  # in seconds
    format: str  # e.g., "mp4", "webm"
    createdAt: datetime
    hasAudio: bool = True
    thumbnailUrl: Optional[str] = None

class InsertRecording(BaseModel):
    title: str
    filename: str
    fileSize: int
    duration: int
    format: str
    hasAudio: Optional[bool] = True
    thumbnailUrl: Optional[str] = None

class ClientMetadata(BaseModel):
    title: str
    filename: str
    duration: int
    format: str
    hasAudio: Optional[bool] = True
    thumbnailUrl: Optional[str] = None

class RecordingOptions(BaseModel):
    screenSource: Literal["entire", "window", "tab"]
    includeMicrophone: bool
    includeSystemAudio: bool
    microphoneVolume: int = Field(..., ge=0, le=100)
    format: Literal["mp4", "webm"]
