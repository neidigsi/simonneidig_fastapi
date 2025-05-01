# Import external dependencies
from sqlalchemy import Table, Column, Integer, ForeignKey

# Import internal dependencies
from app.db.database import Base

# Define the association table for the many-to-many relationship between Work and Category
work_category = Table(
    'work_category',
    Base.metadata,
    Column('work_id', Integer, ForeignKey('work.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)
