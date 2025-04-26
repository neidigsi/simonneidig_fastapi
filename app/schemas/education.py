# Import external dependencies
from pydantic import BaseModel
import datetime

# Import internal dependencies
from app.schemas.institution import Institution


class EducationBase(BaseModel):
    id: int


class Education(EducationBase):
    degree: str | None = None
    grade: float | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    course_of_study: str | None = None
    description: str | None = None
    university: Institution | None = None

    class Config:
        orm_mode = True
