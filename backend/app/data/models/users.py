from datetime import datetime
from pydantic import BaseModel

class CandidateBaseDto(BaseModel):
    name: str
    email: str

# For POST requests
class CandidateCreateDto(CandidateBaseDto):
    pass

# For API responses
class CandidateResponseDto(CandidateBaseDto):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True