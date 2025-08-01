from datetime import datetime
from pydantic import BaseModel

class UserBaseDto(BaseModel):
    name: str
    email: str

# For POST requests
class UserCreateDto(UserBaseDto):
    pass

# For API responses
class UserResponseDto(UserBaseDto):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True