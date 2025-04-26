from sqlalchemy import Column, Double, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.db.models.institution import Institution
from app.db.models.education_translation import EducationTranslation


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    degree = Column(String)
    grade = Column(Double)
    translations = relationship("EducationTranslation", back_populates="education")

    institution_id = Column(Integer, ForeignKey("institution.id"))

    university = relationship(Institution, back_populates="educations")
