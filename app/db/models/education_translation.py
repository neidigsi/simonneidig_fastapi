from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class EducationTranslation(Base):
    __tablename__ = "education_translation"

    id = Column(Integer, primary_key=True)
    education_id = Column(Integer, ForeignKey("education.id"))
    course_of_study = Column(String)
    description = Column(String)
    language = Column(String)
    
    education = relationship(
        "Education", back_populates="translations")