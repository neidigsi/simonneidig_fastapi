"""
Contact DB model for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module defines the Contact SQLAlchemy model which represents contact inquiries
submitted via the website's contact form. Contact records store sender information,
message content, timestamps and the language association. These records are persisted
and can be queried by the API to display or process incoming inquiries.
"""

# Import external dependencies
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Contact(Base):
    __tablename__ = "contact"

    """
    Database object: Contact

    Represents a contact inquiry submitted through the website contact form.

    Attributes:
        id (int): Primary key.
        creation_date (datetime): Timestamp when the entry was created.
        sending_date (datetime | None): Timestamp when the message was sent/processed.
        send (bool): Flag indicating whether the message has been sent or processed.
        name (str): Sender's name.
        email (str): Sender's email address.
        message (str): The message body.
        language_id (int): Foreign key referencing Language for localization.

    Relationships:
        language: Relationship to the Language model (contact.language).
    """

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    creation_date = Column(DateTime)
    sending_date = Column(DateTime)
    send = Column(Boolean)
    name = Column(String)
    email = Column(String)
    message = Column(String)

    # Foreign keys
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    language = relationship(
        "Language", back_populates="contact")
