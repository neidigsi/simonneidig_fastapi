"""
Work DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines the Work model which represents a portfolio item or project shown on the website.
A Work can have translations, a thumbnail image, and belong to multiple categories.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.image import Image

# Define the association table for the many-to-many relationship between Work and Category
work_category = Table(
    'work_category',
    Base.metadata,
    Column('work_id', Integer, ForeignKey('work.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)


class Work(Base):
    __tablename__ = "work"

    """
    Database object: Work

    Represents a portfolio entry or project.

    Attributes:
        id (int): Primary key.
        url (str): External URL to the project or demo.
        thumbnail_id (int): FK to Image used as thumbnail.

    Relationships:
        translations: localized titles/descriptions (WorkTranslation).
        thumbnail: Image used as thumbnail (one-to-one-ish).
        categories: many-to-many relationship to Category.
    """

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    url = Column(String)
    thumbnail_id = Column(Integer, ForeignKey("image.id"))

    # Establishing relationships
    translations = relationship(
        "WorkTranslation", back_populates="work")
    thumbnail = relationship(
        "Image", back_populates="work"
    )
    categories = relationship(
        "Category",
        secondary=work_category,  # Reference the association table directly
        back_populates="works"
    )
