"""
Author: Simon Neidig <mail@simonneidig.de>

Description:
This module defines the Pydantic schemas for the "Work" entity used in the application.
The schemas are used for data validation and serialization/deserialization of work-related data.
"""

# Import external dependencies
from pydantic import BaseModel

# Import internal dependencies
from app.schemas.category import Category


class WorkBase(BaseModel):
    """
    Base model for a work record.

    Attributes:
        id (int): The unique identifier for the work record.
    """
    id: int


class Work(WorkBase):
    """
    Extended model for a work record.

    Attributes:
        title (str | None): The title of the work.
        url (str | None): The URL associated with the work.
        thumbnail (str | None): The thumbnail image URL for the work.
        categories (list[Category] | None): A list of categories associated with the work.
    """
    title: str | None = None
    url: str | None = None
    thumbnail_id: int | None = None
    categories: list[Category] | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True
