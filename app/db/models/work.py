# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.image import Image

# Define the association table for the many-to-many relationship between Work and Category
work_category = Table(
    'work_category',
    Base.metadata,
    Column('work_id', Integer, ForeignKey('work.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)


class Work(Base):
    __tablename__ = "work"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    url = Column(String)
    thumbnail_id = Column(Integer, ForeignKey("image.id"))

    # Establishing relationships
    translations = relationship(
        "WorkTranslation", back_populates="work")
    thumbnail = relationship(
        "Image", back_populates="work"
    )
    categories = relationship(
        "Category",
        secondary=work_category,  # Reference the association table directly
        back_populates="works"
    )
