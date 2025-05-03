# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class PersonalInformation(Base):
    __tablename__ = "personal_information"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    icon = Column(String)

    # Establishing relationships
    translations = relationship(
        "PersonalInformationTranslation", back_populates="personal_information")
