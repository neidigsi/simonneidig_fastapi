# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Expertise(Base):
    __tablename__ = "expertise"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    icon = Column(String)

    # Establishing relationships
    translations = relationship(
        "ExpertiseTranslation", back_populates="expertise")
