# Import external dependencies
from sqlalchemy import Table, Column, Integer, ForeignKey

# Import internal dependencies
from app.db.database import Base

def get_work_category_table(metadata):
    """
    Returns the association table for the many-to-many relationship between Work and Category.
    Ensures that the table is created after the dependent tables (work and category).
    """
    return Table(
        'work_category',
        metadata,
        Column('work_id', Integer, ForeignKey('work.id'), primary_key=True),
        Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
    )

# Use the function to define the table
work_category = get_work_category_table(Base.metadata)
