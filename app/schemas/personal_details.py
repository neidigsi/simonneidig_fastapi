"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
This module defines Pydantic models for representing personal information data.

The `PersonalDetailsBase` class provides the base structure for personal details,
while the `PersonalDetails` class extends it with additional fields, including
the name, position, and abstract. These models are used for data validation
and serialization in the application.
"""

# Import external dependencies
from pydantic import BaseModel


class PersonalDetailsBase(BaseModel):
    """
    Base model for personal details.

    Attributes:
        id (int): The unique identifier for the personal details record.
    """
    id: int


class PersonalDetails(PersonalDetailsBase):
    """
    Extended model for personal details with additional fields.

    Attributes:
        name (str | None): The name of the individual.
        position (str | None): The position or title of the individual.
        abstract (str | None): A brief abstract or summary about the individual.
    """
    name: str | None = None
    position: str | None = None
    abstract: str | None = None
    profile_picture_id: int | None = None


    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True
