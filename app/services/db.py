"""
Author: Simon Neidig <mail@simonneidig.de>

Description:
This module provides a utility function to manage database sessions.

The `get_db` function is a dependency that can be used in FastAPI routes
to provide a database session. It ensures that the session is properly
opened and closed, preventing resource leaks.
"""

from app.db.database import SessionLocal


def get_db():
    """
    Dependency function to provide a database session.

    Yields:
        Session: A SQLAlchemy database session.

    Ensures that the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
