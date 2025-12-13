"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
"""

# Import external dependencies
from pydantic import BaseModel, EmailStr
import datetime

class ContactBase(BaseModel):
    """
    Base model for a contact record.

    Attributes:
        id (int): The unique identifier for the contact record.
    """
    id: int


class ContactRead(ContactBase):
    """
    Extended model for a contact record with additional fields.
    """
    creation_date: datetime.datetime | None = None
    sending_date: datetime.datetime | None = None
    send: bool | None = None
    name: str | None = None
    email: str | None = None
    message: str | None = None
    lang: str | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True


class SendingContact(BaseModel):
    """
    """
    name: str | None = None
    email: EmailStr | None = None
    message: str | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True
