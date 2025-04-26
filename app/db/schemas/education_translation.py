from pydantic import BaseModel


class EducationTranslationBase(BaseModel):
    id: int


class EducationTranslation(EducationTranslationBase):
    education_id: int

    class Config:
        orm_mode = True
