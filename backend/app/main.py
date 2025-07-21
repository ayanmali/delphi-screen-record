# Runs on port 8000 by default

import logging
import sys
from contextlib import asynccontextmanager

from typing import Annotated

from data.models import InsertRecording
from sqlmodel import select
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.database import sessionmanager, get_db_session

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()

app = FastAPI(lifespan=lifespan, title="Delphi Screen Rec", docs_url="/api/docs")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def get_db():
    return "test"

# @app.on_event("startup")
# async def on_startup():
#     await create_db_and_tables()

# @app.on_event("shutdown")
# async def on_shutdown():
#     await shutdown_db_connection()

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# @app.get("/api/recordings", response_model=list[Recording])
# def get_recordings(
#     session: SessionDep, 
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,):
#     recordings = session.exec(select(Recording).offset(offset).limit(limit)).all()
#     return recordings

@app.post("/api/recordings", response_model=InsertRecording)
async def create_recording(recording: InsertRecording, session: SessionDep):
    return recording

@app.post("/api/recordings", response_model=InsertRecording)
async def create_recording(recording: InsertRecording, session: SessionDep):
    db_rec = InsertRecording.model_validate(recording)
    session.add(db_rec)
    session.commit()
    session.refresh(db_rec)
    return db_rec

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {
#         "item_id": item_id,
#         "value": items[item_id],
#         "q": q,
#     }