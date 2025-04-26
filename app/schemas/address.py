# Import external dependencies
from pydantic import BaseModel


class AddressBase(BaseModel):
    id: int


class Address(AddressBase):
    street: str | None = None
    number: int | None = None
    zip: int | None = None
    city: str | None = None
    country: str | None = None
    
    class Config:
        orm_mode = True
