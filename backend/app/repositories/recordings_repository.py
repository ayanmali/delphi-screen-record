from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.data.schemas.recordings import Recording
from app.data.models.recordings import InsertRecordingDto, ClientMetadataDto
from fastapi import HTTPException
from datetime import datetime
from typing import List, Optional

async def create_recording(db_session: AsyncSession, recording: InsertRecordingDto):
    """Create a new recording in the database"""
    db_recording = Recording(
        title=recording.title,
        filename=recording.filename,
        fileSize=recording.fileSize,
        duration=recording.duration,
        format=recording.format,
        hasAudio=recording.hasAudio,
        thumbnailUrl=recording.thumbnailUrl,
        createdAt=datetime.now()
    )
    db_session.add(db_recording)
    await db_session.commit()
    await db_session.refresh(db_recording)
    return db_recording

async def get_recording(db_session: AsyncSession, recording_id: int):
    """Get a specific recording by ID"""
    recording = (await db_session.scalars(select(Recording).where(Recording.id == recording_id))).first()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    return recording

async def get_recording_by_filename(db_session: AsyncSession, filename: str):
    """Get a recording by filename"""
    return (await db_session.scalars(select(Recording).where(Recording.filename == filename))).first()

async def get_all_recordings(db_session: AsyncSession, skip: int = 0, limit: int = 100):
    """Get all recordings with pagination"""
    return (await db_session.scalars(select(Recording).offset(skip).limit(limit))).all()

async def update_recording(db_session: AsyncSession, recording_id: int, recording_data: dict):
    """Update a recording by ID"""
    recording = await get_recording(db_session, recording_id)
    
    for field, value in recording_data.items():
        if hasattr(recording, field):
            setattr(recording, field, value)
    
    await db_session.commit()
    await db_session.refresh(recording)
    return recording

async def delete_recording(db_session: AsyncSession, recording_id: int):
    """Delete a recording by ID"""
    recording = await get_recording(db_session, recording_id)
    await db_session.delete(recording)
    await db_session.commit()
    return True

async def get_recordings_by_format(db_session: AsyncSession, format: str, skip: int = 0, limit: int = 100):
    """Get recordings filtered by format"""
    return (await db_session.scalars(
        select(Recording).where(Recording.format == format).offset(skip).limit(limit)
    )).all()

async def get_recordings_with_audio(db_session: AsyncSession, has_audio: bool = True, skip: int = 0, limit: int = 100):
    """Get recordings filtered by audio presence"""
    return (await db_session.scalars(
        select(Recording).where(Recording.hasAudio == has_audio).offset(skip).limit(limit)
    )).all()

async def search_recordings_by_title(db_session: AsyncSession, title_query: str, skip: int = 0, limit: int = 100):
    """Search recordings by title (case-insensitive partial match)"""
    return (await db_session.scalars(
        select(Recording).where(Recording.title.ilike(f"%{title_query}%")).offset(skip).limit(limit)
    )).all()

async def get_recordings_by_date_range(db_session: AsyncSession, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100):
    """Get recordings within a date range"""
    return (await db_session.scalars(
        select(Recording).where(
            Recording.createdAt >= start_date,
            Recording.createdAt <= end_date
        ).offset(skip).limit(limit)
    )).all()

async def get_recordings_count(db_session: AsyncSession):
    """Get total count of recordings"""
    result = await db_session.scalar(select(Recording.id))
    return result if result else 0