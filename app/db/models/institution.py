# Import external dependencies
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Institution(Base):
    __tablename__ = "institution"

    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Foreign keys
    address_id = Column(Integer, ForeignKey("institution.id"))

    # Establishing relationships
    translations = relationship(
        "InstitutionTranslation", back_populates="institution")
    address = relationship(
        "Address", back_populates="institutions")
    educations = relationship("Education", back_populates="university")
