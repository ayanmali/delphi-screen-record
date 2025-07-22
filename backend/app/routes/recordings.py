# from fastapi import APIRouter, Depends
# from data.models import InsertRecording, Recording
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import Annotated
# from data.database import session_manager

# SessionDep = Annotated[AsyncSession, Depends(session_manager.session)]

# recordings_router = APIRouter(
#     prefix="/api/recordings",
#     tags=["recordings"],
#     responses={404: {"description": "Not found"}},
# )

# # @router.get(
# #     "/{user_id}",
# #     response_model=User,
# #     dependencies=[Depends(validate_is_authenticated)],
# # )
# # async def user_details(
# #     user_id: int,
# #     db_session: DBSessionDep,
# # ):
# #     """
# #     Get any user details
# #     """
# #     user = await get_user(db_session, user_id)
# #     return user

# # @recordings_router.post("", response_model=Recording)
# # async def create_recording(recording: InsertRecording, session: SessionDep):
# #     db_rec = Recording(**recording.model_dump())  # Use Recording, not InsertRecording
# #     session.add(db_rec)
# #     await session.commit()
# #     await session.refresh(db_rec)
# #     return db_rec


# @recordings_router.post("/", response_model=Recording)
# async def create_recording(recording: InsertRecording, session: SessionDep):
#     db_rec = Recording(**recording.model_dump())
#     session.add(db_rec)
#     await session.commit()
#     await session.refresh(db_rec)
#     return db_rec

# # @recordings_router.get("/")
# # async def get_recordings(session: SessionDep):
# #     return "wfqfqgqgq"