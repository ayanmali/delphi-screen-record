from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

# For POST requests
class UserCreate(UserBase):
    pass

# For API responses
class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True