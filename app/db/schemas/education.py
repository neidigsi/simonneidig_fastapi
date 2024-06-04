from pydantic import BaseModel
from app.db.schemas.institution import Institution


class EducationBase(BaseModel):
    id: int


class Education(EducationBase):
    degree: str | None = None
    course_of_study: str | None = None
    description: str | None = None
    university: Institution | None = None

    class Config:
        orm_mode = True
