"""
CategoryTranslation DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines localized names for Category entries.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.category import Category  # Ensure Category is imported

class CategoryTranslation(Base):
    __tablename__ = "category_translation"

    """
    Database object: CategoryTranslation

    Stores the localized name for a Category.

    Attributes:
        id (int): Primary key.
        name (str): Localized category name.
        category_id (int): FK to Category.
        language_id (int): FK to Language.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    name = Column(String)

    # Foreign keys
    category_id = Column(Integer, ForeignKey("category.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    category = relationship(
        "Category", back_populates="translations")
    language = relationship(
        "Language", back_populates="category_translations")
