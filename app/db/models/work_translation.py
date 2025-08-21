"""
WorkTranslation DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

Defines localized titles for Work (portfolio) entries. Each translation associates
a Work with a Language and contains the localized title.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.work import Work


class WorkTranslation(Base):
    __tablename__ = "work_translation"

    """
    Database object: WorkTranslation

    Stores the localized title for a Work entry.

    Attributes:
        id (int): Primary key.
        title (str): Localized title.
        work_id (int): FK to Work.
        language_id (int): FK to Language.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    title = Column(String)

    # Foreign keys
    work_id = Column(Integer, ForeignKey("work.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    work = relationship(
        "Work", back_populates="translations")
    language = relationship(
        "Language", back_populates="work_translations")
