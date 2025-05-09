# Import external dependencies
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Contact(Base):
    __tablename__ = "contact"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    creation_date = Column(DateTime)  # Changed to DateTime
    sending_date = Column(DateTime)  # Changed to DateTime
    sended = Column(Boolean)
    name = Column(String)
    email = Column(String)
    message = Column(String)

    # Foreign keys
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    language = relationship(
        "Language", back_populates="contact")
