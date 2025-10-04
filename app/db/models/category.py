"""
Category DB model for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module defines categories used to classify works or projects.
"""

# Import external dependencies
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Category(Base):
    __tablename__ = "category"

    """
    Database object: Category

    Represents a category/classification for Work entries.

    Attributes:
        id (int): Primary key.

    Relationships:
        translations: localized category names.
        works: many-to-many link to Work.
    """

    # Primary key
    id = Column(Integer, primary_key=True)

    # Establishing relationships
    translations = relationship(
        "CategoryTranslation", back_populates="category"
    )
    works = relationship(
        "Work",
        secondary="work_category",  # Use string reference to avoid circular import
        back_populates="categories"
    )
