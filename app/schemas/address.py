"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
This module defines Pydantic models for representing address data.

The `AddressBase` class provides the base structure for an address,
while the `Address` class extends it with additional optional fields.
These models are used for data validation and serialization in the application.
"""

# Import external dependencies
from pydantic import BaseModel


class AddressBase(BaseModel):
    """
    Base model for an address.

    Attributes:
        id (int): The unique identifier for the address.
    """
    id: int


class Address(AddressBase):
    """
    Extended model for an address with additional optional fields.

    Attributes:
        street (str | None): The street name.
        number (int | None): The house or building number.
        zip (int | None): The postal code.
        city (str | None): The city name.
        country (str | None): The country name.
    """
    street: str | None = None
    number: int | None = None
    zip: int | None = None
    city: str | None = None
    country: str | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True
