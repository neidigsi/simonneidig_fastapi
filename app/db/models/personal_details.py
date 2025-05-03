# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class PersonalDetails(Base):
    __tablename__ = "personal_details"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    name = Column(String)

    # Establishing relationships
    translations = relationship(
        "PersonalDetailsTranslation", back_populates="personal_details")
