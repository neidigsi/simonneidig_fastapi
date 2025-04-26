# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Language(Base):
    __tablename__ = "language"

    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Content
    name = Column(String)

    # Establishing relationships
    education_translations = relationship("EducationTranslation", back_populates="language")
