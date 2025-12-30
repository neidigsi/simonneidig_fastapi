# Import external dependencies
# The SQLAlchemy user base is provided by the adapter package `fastapi-users-db-sqlalchemy`
# Install with: pip install fastapi-users-db-sqlalchemy

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String



# Import internal dependencies
from app.db.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name = Column(String)
    last_name = Column(String)