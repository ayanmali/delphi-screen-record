from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.data.schemas.users import UserDBModel
from app.data.models.users import UserCreate
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# async def create_user(db: AsyncSession, user: UserCreate):
#     db_user = User(name=user.name, email=user.email)
#     db.add(db_user)
#     await db.commit()
#     await db.refresh(db_user)
#     return db_user

async def create_user(db_session: AsyncSession, user: UserCreate):
    db_user = UserDBModel(name=user.name, email=user.email)
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user

async def get_user(db_session: AsyncSession, user_id: int):
    user = (await db_session.scalars(select(UserDBModel).where(UserDBModel.id == user_id))).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_user_by_email(db_session: AsyncSession, email: str):
    return (await db_session.scalars(select(UserDBModel).where(UserDBModel.email == email))).first()