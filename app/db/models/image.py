# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.personal_details import PersonalDetails


class Image(Base):
    __tablename__ = "image"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Content
    filename = Column(String, nullable=False, unique=True)
    filepath = Column(String, nullable=False)

    # Establishing relationships
    work = relationship(
        "Work", back_populates="thumbnail", uselist=False
    )
    personal_details = relationship(
        "PersonalDetails", back_populates="profile_picture", uselist=False
    )
