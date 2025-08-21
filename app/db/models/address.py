"""
Address DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines postal/location addresses reused by other entities (e.g., Institution).
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Address(Base):
    __tablename__ = "address"

    """
    Database object: Address

    Represents a postal address record used by institutions.

    Attributes:
        id (int): Primary key.
        street (str): Street name.
        number (str): House/building number.
        zip (int): Postal code.
        city (str): City name.
        country (str): Country code or name.

    Relationships:
        institutions: list of Institution objects linked to this address.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    street = Column(String)
    number = Column(String)
    zip = Column(Integer)
    city = Column(String)
    country = Column(String)

    # Establishing relationships
    institutions = relationship("Institution", back_populates="address")
