"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
This module defines Pydantic models for representing education data.

The `EducationBase` class provides the base structure for an education record,
while the `Education` class extends it with additional fields, including details
about the degree, course of study, and the associated university. These models
are used for data validation and serialization in the application.
"""

# Import external dependencies
from pydantic import BaseModel
import datetime

# Import internal dependencies
from app.schemas.institution import InstitutionRead


class EducationBase(BaseModel):
    """
    Base model for an education record.

    Attributes:
        id (int): The unique identifier for the education record.
    """
    id: int


class EducationRead(EducationBase):
    """
    Extended model for an education record with additional fields.

    Attributes:
        degree (str | None): The degree obtained (e.g., Bachelor's, Master's).
        grade (float | None): The grade achieved.
        start_date (datetime.date | None): The start date of the education.
        end_date (datetime.date | None): The end date of the education.
        course_of_study (str | None): The course of study or major.
        description (str | None): A description of the education.
        university (Institution | None): The associated university, represented as an `Institution` object.
    """
    degree: str | None = None
    grade: float | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    course_of_study: str | None = None
    description: str | None = None
    university: InstitutionRead | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True


class EducationCreate(BaseModel):
    """
    Schema used to create a new Education record together with its
    localized fields.

    Note: The language is taken from the request dependency (`get_language`).
    """
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    degree: str | None = None
    grade: float | None = None
    institution_id: int | None = None

    # localized fields
    course_of_study: str | None = None
    description: str | None = None
