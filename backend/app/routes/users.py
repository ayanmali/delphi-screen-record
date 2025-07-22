from typing import List
from app.dependencies import DBSessionDep
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import user_repository
from app.data.schemas.users import UserDBModel
from app.data.models.users import UserCreate, UserResponse

users_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@users_router.get(
    "/{user_id}",
    response_model=UserResponse,
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

@users_router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate, 
    db_session: DBSessionDep
):
    return await user_repository.create_user(db_session, user=user)

@users_router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int, 
    db_session: DBSessionDep
):
    db_user = await user_repository.get_user(db_session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@users_router.get("/users/", response_model=List[UserResponse])
async def read_users(
    db_session: DBSessionDep,
    skip: int = 0, 
    limit: int = 100, 
):
    users = await user_repository.get_users(db_session, skip=skip, limit=limit)
    return users