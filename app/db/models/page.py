"""
Page DB model for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module defines the Page model representing generic, extendable content pages.
Pages are designed to be used as generic views with localized content.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Page(Base):
    __tablename__ = "page"

    """
    Database object: Page

    Represents a generic content page.

    Attributes:
        id (int): Primary key.
        tech_key (str): Technical key used to reference the page.
        creation_date (date): Date the page was created.

    Relationships:
        translations: localized page content (PageTranslation).
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    tech_key = Column(String)
    creation_date = Column(Date)

    # Establishing relationships
    translations = relationship(
        "PageTranslation", back_populates="page")
