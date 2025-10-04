"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
"""

# Import external dependencies
from pydantic import BaseModel, EmailStr


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
