# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Address(Base):
    __tablename__ = "address"

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
