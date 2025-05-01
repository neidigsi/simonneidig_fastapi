"""
Author: Simon Neidig <mail@simonneidig.de>

Description:
This file defines the Pydantic models used for handling expertise-related data in the FastAPI application.
The models are used to validate and serialize data between the API and the database.
"""

# Import external dependencies
from pydantic import BaseModel

class ExpertiseBase(BaseModel):
    """
    Base model for an expertise record.

    Attributes:
        id (int): The unique identifier for the expertise record.
    """
    id: int

class Expertise(ExpertiseBase):
    """
    Full model for an expertise record.

    Attributes:
        expertise (str | None): The name or title of the expertise.
        description (str | None): A textual description of the expertise.
        icon (str | None): The icon associated with the expertise.
    """
    title: str | None = None
    description: str | None = None 
    icon: str | None = None

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        orm_mode = True
