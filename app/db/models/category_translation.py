# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.category import Category  # Ensure Category is imported

class CategoryTranslation(Base):
    __tablename__ = "category_translation"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    name = Column(String)

    # Foreign keys
    category_id = Column(Integer, ForeignKey("category.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    category = relationship(
        "Category", back_populates="translations")
    language = relationship(
        "Language", back_populates="category_translations")
