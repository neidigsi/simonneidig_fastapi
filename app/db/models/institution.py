"""
Institution DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines institutions (universities, companies) referenced by experiences and educations.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.institution_translation import InstitutionTranslation
from app.db.models.address import Address


class Institution(Base):
    __tablename__ = "institution"

    """
    Database object: Institution

    Represents an institution such as a university or company.

    Attributes:
        id (int): Primary key.
        address_id (int): FK to Address.

    Relationships:
        translations: localized names (InstitutionTranslation).
        address: Address object.
        educations: Education records linked to this institution.
        experiences: Experience records linked to this institution.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Foreign keys
    address_id = Column(Integer, ForeignKey("address.id"))

    # Establishing relationships
    translations = relationship(
        "InstitutionTranslation", back_populates="institution")
    address = relationship(
        "Address", back_populates="institutions")
    educations = relationship("Education", back_populates="university")
    experiences = relationship("Experience", back_populates="company")
