from datetime import datetime
from pydantic import BaseModel

class AssessmentBaseDto(BaseModel):
    id: int
    title: str

class AssessmentCreateDto(AssessmentBaseDto):
    pass

class AssessmentResponseDto(AssessmentBaseDto):
    createdAt: datetime

    class Config:
        from_attributes = True

class AssessmentListResponseDto(BaseModel):
    assessments: list[AssessmentResponseDto]
    total: int
    skip: int
    limit: int