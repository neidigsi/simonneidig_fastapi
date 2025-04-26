# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class EducationTranslation(Base):
    __tablename__ = "education_translation"

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
