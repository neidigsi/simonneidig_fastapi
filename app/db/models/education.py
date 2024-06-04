from sqlalchemy import Column, Double, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.db.models.institution import Institution


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    degree = Column(String)
    course_of_study = Column(String)
    description = Column(String)
    grade = Column(Double)
    institution_id = Column(Integer, ForeignKey("institution.id"))


    university = relationship("Institution", back_populates="educations")