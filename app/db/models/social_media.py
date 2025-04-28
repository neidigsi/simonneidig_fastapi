# Import external dependencies
from sqlalchemy import Column, Integer, String

# Import internal dependencies
from app.db.database import Base


class SocialMedia(Base):
    __tablename__ = "social_media"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    name = Column(String)
    url = Column(String)
    color = Column(String)
    path = Column(String)
