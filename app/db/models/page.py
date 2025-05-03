# Import external dependencies
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Page(Base):
    __tablename__ = "page"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    tech_key = Column(String)
    creation_date = Column(Date)

    # Establishing relationships
    translations = relationship(
        "PageTranslation", back_populates="page")
