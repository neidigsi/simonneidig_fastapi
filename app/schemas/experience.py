"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
This module defines Pydantic models for representing experience data.

The `ExperienceBase` class provides the base structure for an experience record,
while the `Experience` class extends it with additional fields, including details
about the title, description, industry, and the associated company. These models
are used for data validation and serialization in the application.
"""

# Import external dependencies
from pydantic import BaseModel
import datetime

# Import internal dependencies
from app.schemas.institution import InstitutionRead


class ExperienceBase(BaseModel):
    """
    Base model for an experience record.

    Attributes:
        id (int): The unique identifier for the experience record.
    """
    id: int


class ExperienceRead(ExperienceBase):
    """
    Extended model for an experience record with additional fields.

    Attributes:
        title (str | None): The title of the experience.
        extract (str | None): A short summary or extract of the experience.
        description (str | None): A detailed description of the experience.
        industry (str | None): The industry associated with the experience.
        url (str | None): A URL related to the experience (e.g., company website).
        start_date (datetime.date | None): The start date of the experience.
        end_date (datetime.date | None): The end date of the experience.
        company (Institution | None): The associated company, represented as an `Institution` object.
    """
    title: str | None = None
    extract: str | None = None
    description: str | None = None
    industry: str | None = None
    url: str | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    company: InstitutionRead | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True


class ExperienceCreate(BaseModel):
    """
    Schema used to create a new Experience record together with its
    localized fields.

    Note: The language is taken from the request dependency (`get_language`).
    """
    url: str | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    institution_id: int | None = None
    
    # localized fields
    title: str | None = None
    extract: str | None = None
    description: str | None = None
    industry: str | None = None