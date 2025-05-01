# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.work import Work


class WorkTranslation(Base):
    __tablename__ = "work_translation"

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
