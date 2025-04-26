# Import external dependencies
from sqlalchemy import Column, Double, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.institution import Institution


class Education(Base):
    __tablename__ = "education"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    start_date = Column(Date)
    end_date = Column(Date)
    degree = Column(String)
    grade = Column(Double)

    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institution.id"))

    # Establishing relationships
    translations = relationship(
        "EducationTranslation", back_populates="education")
    university = relationship(Institution, back_populates="educations")
