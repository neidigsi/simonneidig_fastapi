"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
This module defines Pydantic models for representing institution data.

The `InstitutionBase` class provides the base structure for an institution,
while the `Institution` class extends it with additional fields, including
the name and address. These models are used for data validation and serialization
in the application.
"""

# Import external dependencies
from pydantic import BaseModel

# Import internal dependencies
from app.schemas.address import Address


class InstitutionBase(BaseModel):
    """
    Base model for an institution.

    Attributes:
        id (int): The unique identifier for the institution.
    """
    id: int


class InstitutionRead(InstitutionBase):
    """
    Extended model for an institution with additional fields.

    Attributes:
        name (str | None): The name of the institution.
        address (Address | None): The address of the institution, represented as an `Address` object.
    """
    name: str | None = None
    address: Address | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True
        
        
class InstitutionCreate(BaseModel):
    """
    Schema used to create a new Institution record together with its
    localized fields.

    Note: The language is taken from the request dependency (`get_language`).
    """
    address_id: int | None = None
    
    # localized fields
    name: str | None = None
