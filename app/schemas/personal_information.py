"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
This module defines Pydantic models for representing personal information data.

The `PersonalInformationsBase` class provides the base structure for personal information,
while the `PersonalInformation` class extends it with additional fields, including
the label, value, and icon. These models are used for data validation
and serialization in the application.
"""

# Import external dependencies
from pydantic import BaseModel


class PersonalInformationsBase(BaseModel):
    """
    Base model for personal information.

    Attributes:
        id (int): The unique identifier for the personal information record.
    """
    id: int


class PersonalInformationRead(PersonalInformationsBase):
    """
    Extended model for personal information with additional fields.

    Attributes:
        label (str | None): The label or key for the personal information.
        value (str | None): The value or content of the personal information.
        icon (str | None): The icon associated with the personal information.
    """
    label: str | None = None
    value: str | None = None
    icon: str | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True


class PersonalInformationCreate(BaseModel):
    """
    Schema used to create a new personal information record together with its
    localized fields.

    Note: The language is taken from the request dependency (`get_language`).
    """
    label: str | None = None
    value: str | None = None 
    icon: str | None = None
