from pydantic import BaseModel


class InstitutionBase(BaseModel):
    id: int


class Institution(InstitutionBase):
    name: str | None = None
    description: str | None = None

    class Config:
        orm_mode = True
