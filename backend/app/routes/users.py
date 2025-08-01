from typing import List
from app.dependencies import DBSessionDep
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import user_repository
from app.data.schemas.users import User
from app.data.models.users import UserCreateDto, UserResponseDto

users_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@users_router.get(
    "/{user_id}",
    response_model=UserResponseDto,
)
async def user_details(
    user_id: int,
    db_session: DBSessionDep,
):
    """
    Get any user details
    """
    user = await user_repository.get_user(db_session, user_id)
    return user

@users_router.post("/", response_model=UserResponseDto)
async def create_user(
    user: UserCreateDto, 
    db_session: DBSessionDep
):
    return await user_repository.create_user(db_session, user=user)

@users_router.get("/users/{user_id}", response_model=UserResponseDto)
async def read_user(
    user_id: int, 
    db_session: DBSessionDep
):
    db_user = await user_repository.get_user(db_session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@users_router.get("/users/", response_model=List[UserResponseDto])
async def read_users(
    db_session: DBSessionDep,
    skip: int = 0, 
    limit: int = 100, 
):
    users = await user_repository.get_users(db_session, skip=skip, limit=limit)
    return users