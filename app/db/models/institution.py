from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Institution(Base):
    __tablename__ = "institution"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    educations = relationship("Education", back_populates="university")
