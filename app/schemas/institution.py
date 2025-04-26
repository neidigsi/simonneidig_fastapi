# Import external dependencies
from pydantic import BaseModel

# Import internal dependencies
from app.schemas.address import Address


class InstitutionBase(BaseModel):
    id: int


class Institution(InstitutionBase):
    name: str | None = None
    description: str | None = None
    address: Address | None = None

    class Config:
        orm_mode = True
