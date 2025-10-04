"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
This module defines Pydantic models for representing social media data.

The `SocialMediaBase` class provides the base structure for a social media record,
while the `SocialMedia` class extends it with additional fields, including details
about the name, URL, color, and path. These models are used for data validation
and serialization in the application.
"""

# Import external dependencies
from pydantic import BaseModel


class SocialMediaBase(BaseModel):
    """
    Base model for a social media record.

    Attributes:
        id (int): The unique identifier for the social media record.
    """
    id: int


class SocialMediaRead(SocialMediaBase):
    """
    Extended model for a social media record with additional fields.

    Attributes:
        name (str | None): The name of the social media platform.
        url (str | None): The URL of the social media platform.
        color (str | None): The color associated with the platform (e.g., branding color).
        path (str | None): The path or icon name for the platform.
    """
    name: str | None = None
    url: str | None = None
    color: str | None = None
    path: str | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True
        
        
        
class SocialMediaCreate(BaseModel):
    """
    Extended model for a social media record with additional fields.

    Attributes:
        name (str | None): The name of the social media platform.
        url (str | None): The URL of the social media platform.
        color (str | None): The color associated with the platform (e.g., branding color).
        path (str | None): The path or icon name for the platform.
    """
    name: str | None = None
    url: str | None = None
    color: str | None = None
    path: str | None = None

