# # backend/app/db.py
# import os
# from datetime import datetime
# from typing import Literal
# from sqlmodel import Field, SQLModel
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from dotenv import load_dotenv
# from sqlalchemy.orm import sessionmaker

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL", "")
# print("DATABASE_URL: ", DATABASE_URL)

# # connect_args = {"check_same_thread": False}
# engine = create_async_engine(DATABASE_URL, echo=True, future=True)
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# # Schema
# class Recording(SQLModel, table=True):
#     __tablename__ = "recordings"
#     id: int = Field(primary_key=True)
#     title: str = Field(index=True)
#     filename: str = Field(index=True)
#     fileSize: int = Field(index=True)
#     duration: int = Field(index=True)
#     format: str = Field(index=True) # e.g. "mp4", "webm"
#     createdAt: datetime = Field(index=True)
#     hasAudio: bool = Field(index=True)
#     thumbnailUrl: str | None = Field(index=True)

# # Data Transfer Objects
# class InsertRecording(SQLModel, table=False):
#     title: str = Field(index=True)
#     filename: str = Field(index=True)
#     fileSize: int = Field(index=True)
#     duration: int = Field(index=True)
#     format: str = Field(index=True)
#     hasAudio: bool = Field(index=True)
#     thumbnailUrl: str | None = Field(index=True)

# class ClientMetadata(SQLModel, table=False):
#     title: str = Field(index=True)
#     filename: str = Field(index=True)
#     duration: int = Field(index=True)
#     format: str = Field(index=True)
#     hasAudio: bool = Field(index=True)
#     thumbnailUrl: str | None = Field(index=True)

# class RecordingOptions(SQLModel, table=False):
#     screenSource: Literal["entire", "window", "tab"] = Field(index=True)
#     includeMicrophone: bool = Field(index=True)
#     includeSystemAudio: bool = Field(index=True)
#     microphoneVolume: int = Field(..., ge=0, le=100, index=True)
#     format: Literal["mp4", "webm"] = Field(index=True)

# # Database functions
# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)

# async def shutdown_db_connection():
#     await engine.dispose()

# async def get_session():
#     async with async_session() as session:
#         yield session