# Data Transfer Objects
from typing import Literal
from pydantic import BaseModel

class RecordingBase(BaseModel):
    title: str
    filename: str
    fileSize: int
    duration: int
    format: str
    hasAudio: bool
    thumbnailUrl: str | None

class InsertRecording(RecordingBase):
    pass

class ClientMetadata(RecordingBase):
    pass

class RecordingOptions(BaseModel):
    screenSource: Literal["entire", "window", "tab"]
    includeMicrophone: bool
    includeSystemAudio: bool
    microphoneVolume: int
    format: Literal["mp4", "webm"]