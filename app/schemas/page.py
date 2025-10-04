"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
This module defines Pydantic models for representing page data.

The `PageBase` class provides the base structure for a page, while the `Page` class
extends it with additional fields, including technical key, title, abstract, HTML content,
and creation date. These models are used for data validation and serialization in the application.

Purpose:
The `Page` schema is designed to represent pages with localized content, allowing the application
to handle multilingual data and provide structured responses for API consumers.

Functionality:
- `PageBase`: Defines the core attributes of a page, such as its unique identifier.
- `Page`: Extends the base model with additional attributes, enabling the representation of
  detailed page information, including metadata and content.
"""

# Import external dependencies
from pydantic import BaseModel
import datetime


class PageBase(BaseModel):
    """
    Base model for a page.

    Attributes:
        id (int): The unique identifier for the page.
    """
    id: int


class Page(PageBase):
    """
    Extended model for a page with additional fields.

    Attributes:
        tech_key (str | None): A technical key for identifying the page.
        title (str | None): The title of the page.
        abstract (str | None): A brief abstract or summary of the page.
        html (str | None): The HTML content of the page.
        creation_date (datetime.date | None): The creation date of the page.
    """
    tech_key: str | None = None
    title: str | None = None
    abstract: str | None = None
    html: str | None = None
    creation_date: datetime.date | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True
