"""
Social Media DB model for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module defines the SocialMedia SQLAlchemy model used to store links to social profiles
displayed on the website (e.g., LinkedIn, GitHub, Instagram). Each record contains a display
name, the target URL, an optional color for UI rendering and an SVG path used to render an icon.
These records are returned to the frontend and rendered in the site's sidebar and footer.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String

# Import internal dependencies
from app.db.database import Base


class SocialMedia(Base):
    __tablename__ = "social_media"

    """
    Database object: SocialMedia

    Represents a social media profile/link used on the website.

    Attributes:
        id (int): Primary key.
        name (str): Human-readable name of the social network (e.g., 'LinkedIn').
        url (str): Target URL of the profile.
        color (str): Optional brand color or hex value for UI rendering.
        path (str): SVG path data used to render an icon for the network.
    """

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    name = Column(String)
    url = Column(String)
    color = Column(String)
    path = Column(String)
