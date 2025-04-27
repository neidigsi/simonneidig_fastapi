# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.education_translation import EducationTranslation
from app.db.models.experience_translation import ExperienceTranslation


class Language(Base):
    __tablename__ = "language"

    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Content
    name = Column(String)
    iso639_1 = Column(String)

    # Establishing relationships
    education_translations = relationship("EducationTranslation", back_populates="language")
    experience_translations = relationship("ExperienceTranslation", back_populates="language")
    institution_translations = relationship("InstitutionTranslation", back_populates="language")
