# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class ExperienceTranslation(Base):
    __tablename__ = "experience_translation"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    title = Column(String)
    extract = Column(String)
    description = Column(String)
    industry = Column(String)

    # Foreign keys
    experience_id = Column(Integer, ForeignKey("experience.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    experience = relationship(
        "Experience", back_populates="translations")
    language = relationship(
        "Language", back_populates="experience_translations")
