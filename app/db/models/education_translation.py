"""
EducationTranslation DB model for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module defines localized course/description entries for Education records.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.education import Education


class EducationTranslation(Base):
    __tablename__ = "education_translation"

    """
    Database object: EducationTranslation

    Stores localized course_of_study and description.

    Attributes:
        id (int): Primary key.
        course_of_study (str): Localized course name.
        description (str): Localized description.
        education_id (int): FK to Education.
        language_id (int): FK to Language.
    """

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    course_of_study = Column(String)
    description = Column(String)

    # Foreign keys
    education_id = Column(Integer, ForeignKey("education.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    education = relationship(
        "Education", back_populates="translations")
    language = relationship(
        "Language", back_populates="education_translations")
