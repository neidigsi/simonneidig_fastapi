# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.category_translation import CategoryTranslation
from app.db.models.education_translation import EducationTranslation
from app.db.models.experience_translation import ExperienceTranslation
from app.db.models.expertise_translation import ExpertiseTranslation
from app.db.models.personal_details_translation import PersonalDetailsTranslation
from app.db.models.personal_information_translation import PersonalInformationTranslation
from app.db.models.work_translation import WorkTranslation


class Language(Base):
    __tablename__ = "language"

    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Content
    name = Column(String)
    iso639_1 = Column(String)

    # Establishing relationships
    category_translations = relationship("CategoryTranslation", back_populates="language")
    education_translations = relationship("EducationTranslation", back_populates="language")
    experience_translations = relationship("ExperienceTranslation", back_populates="language")
    expertise_translations = relationship("ExpertiseTranslation", back_populates="language")
    institution_translations = relationship("InstitutionTranslation", back_populates="language")
    personal_details_translations = relationship("PersonalDetailsTranslation", back_populates="language")
    personal_information_translations = relationship("PersonalInformationTranslation", back_populates="language")
    work_translations = relationship("WorkTranslation", back_populates="language")
