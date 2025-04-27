# Import external dependencies
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Experience(Base):
    __tablename__ = "experience"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    start_date = Column(Date)
    end_date = Column(Date)
    url = Column(String)

    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institution.id"))

    # Establishing relationships
    translations = relationship(
        "ExperienceTranslation", back_populates="experience")
    company = relationship("Institution", back_populates="experiences")
