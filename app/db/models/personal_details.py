# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class PersonalDetails(Base):
    __tablename__ = "personal_details"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    name = Column(String)
    profile_picture_id = Column(Integer, ForeignKey("image.id"))

    # Establishing relationships
    profile_picture = relationship(
        "Image", back_populates="personal_details"
    )
    translations = relationship(
        "PersonalDetailsTranslation", back_populates="personal_details")
