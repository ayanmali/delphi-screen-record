from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.data.schemas.users import Candidate
from app.data.models.users import CandidateCreateDto
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(db_session: AsyncSession, user: CandidateCreateDto):
    db_user = Candidate(name=user.name, email=user.email)
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user

async def get_user(db_session: AsyncSession, user_id: int):
    user = (await db_session.scalars(select(Candidate).where(Candidate.id == user_id))).first()
    if not user:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return user

async def get_user_by_email(db_session: AsyncSession, email: str):
    return (await db_session.scalars(select(Candidate).where(Candidate.email == email))).first()

async def get_users(db_session: AsyncSession, skip: int = 0, limit: int = 100):
    return (await db_session.scalars(select(Candidate).offset(skip).limit(limit))).all()