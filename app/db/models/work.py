# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.associations import work_category  # Import work_category

class Work(Base):
    __tablename__ = "work"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    url = Column(String)
    thumbnail = Column(String)

    # Establishing relationships
    translations = relationship(
        "WorkTranslation", back_populates="work")
    categories = relationship(
        "Category",
        secondary=work_category,  # Use the imported work_category table
        back_populates="works"
    )
