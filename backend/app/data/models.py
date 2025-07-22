# from datetime import datetime
# from typing import Literal
# from app.data.database import Base
# from sqlmodel import Field, SQLModel
# from sqlalchemy import Column, Integer, String, DateTime, func

# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional

# class UserBase(BaseModel):
#     name: str
#     email: str

# class UserCreate(UserBase):
#     pass

# class UserResponse(UserBase):
#     id: int
#     created_at: datetime
    
#     class Config:
#         from_attributes = True

# class UserDBModel(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     created_at = Column(DateTime, default=func.now())

# # Schema
# # class Recording(SQLModel, table=True):
# #     __tablename__ = "recordings"
# #     id: int = Field(primary_key=True)
# #     title: str = Field(index=True)
# #     filename: str = Field(index=True)
# #     fileSize: int = Field(index=True)
# #     duration: int = Field(index=True)
# #     format: str = Field(index=True) # e.g. "mp4", "webm"
# #     createdAt: datetime = Field(index=True)
# #     hasAudio: bool = Field(index=True)
# #     thumbnailUrl: str | None = Field(index=True)

# # # Data Transfer Objects
# # class InsertRecording(SQLModel, table=False):
# #     title: str = Field(index=True)
# #     filename: str = Field(index=True)
# #     fileSize: int = Field(index=True)
# #     duration: int = Field(index=True)
# #     format: str = Field(index=True)
# #     hasAudio: bool = Field(index=True)
# #     thumbnailUrl: str | None = Field(index=True)

# # class ClientMetadata(SQLModel, table=False):
# #     title: str = Field(index=True)
# #     filename: str = Field(index=True)
# #     duration: int = Field(index=True)
# #     format: str = Field(index=True)
# #     hasAudio: bool = Field(index=True)
# #     thumbnailUrl: str | None = Field(index=True)

# # class RecordingOptions(SQLModel, table=False):
# #     screenSource: Literal["entire", "window", "tab"] = Field(index=True)
# #     includeMicrophone: bool = Field(index=True)
# #     includeSystemAudio: bool = Field(index=True)
# #     microphoneVolume: int = Field(..., ge=0, le=100, index=True)
# #     format: Literal["mp4", "webm"] = Field(index=True)