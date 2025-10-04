"""
Author: Simon Neidig <mail@simon-neidig.eu>

Description:
This module provides a utility function to manage database sessions.

The `get_async_session` function is a dependency that can be used in FastAPI routes
to provide a database session. It ensures that the session is properly
opened and closed, preventing resource leaks.
"""

# Import internal dependencies
from app.db.database import async_session_maker
from app.db.models.user import User

# Import external dependencies
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        
        
def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)