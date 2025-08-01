# Data Transfer Objects
from typing import Literal
from datetime import datetime
from pydantic import BaseModel

class RecordingBaseDto(BaseModel):
    title: str
    filename: str
    fileSize: int
    duration: int
    format: str
    hasAudio: bool
    thumbnailUrl: str | None

class InsertRecordingDto(RecordingBaseDto):
    pass

class ClientMetadataDto(RecordingBaseDto):
    pass

class RecordingOptionsDto(BaseModel):
    screenSource: Literal["entire", "window", "tab"]
    includeMicrophone: bool
    includeSystemAudio: bool
    microphoneVolume: int
    format: Literal["mp4", "webm"]

class RecordingResponseDto(RecordingBaseDto):
    id: int
    createdAt: datetime

    class Config:
        from_attributes = True

class RecordingListResponseDto(BaseModel):
    recordings: list[RecordingResponseDto]
    total: int
    skip: int
    limit: int