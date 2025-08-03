from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from app.data.schemas.recordings import InsertRecordingDto, ClientMetadataDto, RecordingResponseDto
from app.repositories.recordings_repository import (
    create_recording,
    get_recording,
    get_all_recordings,
    update_recording,
    delete_recording,
    get_recordings_by_format,
    get_recordings_with_audio,
    search_recordings_by_title,
    #get_recordings_by_date_range,
    get_recordings_count
)
from typing import Optional, List
from app.dependencies import DBSessionDep
import json
import os
from datetime import datetime

recordings_router = APIRouter(
    prefix="/api/recordings",
    tags=["recordings"],
    responses={404: {"description": "Not found"}},
)

# Get all recordings
@recordings_router.get("/", response_model=List[RecordingResponseDto])
async def get_recordings(
    session: DBSessionDep,
    skip: int = 0,
    limit: int = 100,
    format: Optional[str] = None,
    has_audio: Optional[bool] = None,
    search: Optional[str] = None
):
    """
    Get all recordings with optional filtering and pagination
    """
    try:
        if format:
            return await get_recordings_by_format(session, format, skip, limit)
        elif has_audio is not None:
            return await get_recordings_with_audio(session, has_audio, skip, limit)
        elif search:
            return await search_recordings_by_title(session, search, skip, limit)
        else:
            return await get_all_recordings(session, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recordings: {e}")

# Get specific recording
@recordings_router.get("/{recording_id}", response_model=RecordingResponseDto)
async def get_recording_by_id(session: DBSessionDep, recording_id: int):
    """
    Get a specific recording by ID
    """
    try:
        return await get_recording(session, recording_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recording: {e}")

# Create new recording
@recordings_router.post("/", response_model=RecordingResponseDto)
async def create_new_recording(
    session: DBSessionDep,
    video: UploadFile = File(...),
    metadata: str = Form(...)
):
    """
    Create a new recording with video file upload
    """
    try:
        if not video:
            raise HTTPException(status_code=400, detail="No video file provided")
        
        # Parse metadata
        try:
            recording_data = json.loads(metadata)
            validated_data = ClientMetadataDto(**recording_data)
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(status_code=400, detail=f"Invalid metadata format: {e}")
        
        # Generate unique filename
        timestamp = int(datetime.now().timestamp() * 1000)
        file_extension = os.path.splitext(video.filename)[1] if video.filename else ".mp4"
        unique_filename = f"recording_{timestamp}{file_extension}"
        
        # Save file to disk (you might want to implement proper file storage)
        recordings_dir = "recordings"
        os.makedirs(recordings_dir, exist_ok=True)
        file_path = os.path.join(recordings_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            content = await video.read()
            buffer.write(content)
        
        # Create recording record
        recording_dto = InsertRecordingDto(
            title=validated_data.title,
            filename=unique_filename,
            fileSize=len(content),
            duration=validated_data.duration,
            format=validated_data.format,
            hasAudio=validated_data.hasAudio,
            thumbnailUrl=validated_data.thumbnailUrl
        )
        
        return await create_recording(session, recording_dto)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save recording: {e}")

# Download recording file
@recordings_router.get("/{recording_id}/download")
async def download_recording(session: DBSessionDep, recording_id: int):
    """
    Download a recording file
    """
    try:
        recording = await get_recording(session, recording_id)
        
        file_path = os.path.join("recordings", recording.filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Recording file not found")
        
        def iterfile():
            with open(file_path, "rb") as file:
                yield from file
        
        return StreamingResponse(
            iterfile(),
            media_type=f"video/{recording.format}",
            headers={"Content-Disposition": f'attachment; filename="{recording.title}.{recording.format}"'}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download recording: {e}")

# Stream recording file
@recordings_router.get("/{recording_id}/stream")
async def stream_recording(session: DBSessionDep, recording_id: int):
    """
    Stream a recording file
    """
    try:
        recording = await get_recording(session, recording_id)
        
        file_path = os.path.join("recordings", recording.filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Recording file not found")
        
        def iterfile():
            with open(file_path, "rb") as file:
                yield from file
        
        return StreamingResponse(
            iterfile(),
            media_type=f"video/{recording.format}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stream recording: {e}")

# Update recording
@recordings_router.put("/{recording_id}", response_model=RecordingResponseDto)
async def update_recording_by_id(
    session: DBSessionDep,
    recording_id: int,
    recording_data: dict
):
    """
    Update a recording by ID
    """
    try:
        return await update_recording(session, recording_id, recording_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update recording: {e}")

# Delete recording
@recordings_router.delete("/{recording_id}")
async def delete_recording_by_id(session: DBSessionDep, recording_id: int):
    """
    Delete a recording by ID
    """
    try:
        recording = await get_recording(session, recording_id)
        
        # Delete file from disk
        file_path = os.path.join("recordings", recording.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        await delete_recording(session, recording_id)
        return {"message": "Recording deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete recording: {e}")

# Get storage statistics
@recordings_router.get("/storage/stats")
async def get_storage_stats(session: DBSessionDep):
    """
    Get storage statistics
    """
    try:
        total_recordings = await get_recordings_count(session)
        total_size = 0
        
        # Calculate total size (you might want to optimize this)
        recordings = await get_all_recordings(session, skip=0, limit=1000)
        for recording in recordings:
            total_size += recording.fileSize
        
        return {
            "totalRecordings": total_recordings,
            "totalSize": total_size,
            "formats": {
                "mp4": len([r for r in recordings if r.format == "mp4"]),
                "webm": len([r for r in recordings if r.format == "webm"])
            },
            "withAudio": len([r for r in recordings if r.hasAudio]),
            "withoutAudio": len([r for r in recordings if not r.hasAudio])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch storage stats: {e}")