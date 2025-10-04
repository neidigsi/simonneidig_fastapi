"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
This module defines the Pydantic schemas for the "Category" entity used in the application.
The schemas are used for data validation and serialization/deserialization of category-related data.
"""

# Import external dependencies
from pydantic import BaseModel


class CategoryBase(BaseModel):
    """
    Base model for a category.

    Attributes:
        id (int): The unique identifier for the category.
    """
    id: int


class Category(CategoryBase):
    """
    Extended schema for a category.

    Attributes:
        name (str | None): The name of the category. This is optional and can be None.
    """
    name: str | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True
