# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.page import Page


class PageTranslation(Base):
    __tablename__ = "page_translation"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    title = Column(String)
    abstract = Column(String)
    html = Column(String)

    # Foreign keys
    page_id = Column(Integer, ForeignKey("page.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    page = relationship(
        "Page", back_populates="translations")
    language = relationship(
        "Language", back_populates="page_translations")
