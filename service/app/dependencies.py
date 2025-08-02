from typing import Annotated

from app.data.database import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Async Database Session Dependency
DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]