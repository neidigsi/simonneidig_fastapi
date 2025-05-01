# Import external dependencies
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Category(Base):
    __tablename__ = "category"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Establishing relationships
    translations = relationship(
        "CategoryTranslation", back_populates="category"
    )
    works = relationship(
        "Work",
        secondary="work_category",  # Use string reference to avoid circular import
        back_populates="categories"
    )
