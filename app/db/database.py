"""
Database configuration and session factory

Author: Simon Neidig <mail@simonneidig.de>

This module configures the SQLAlchemy engine, session factory and declarative base
used throughout the application.

Main features:
- Creates the engine from configuration.
- Exposes a scoped SessionLocal for request-scoped DB sessions.
- Provides the Base declarative class for model definitions.
"""

# Import external dependencies
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


# Import internal dependencies
from app.core import config


# Create database engine and connect to configured db string
engine = create_async_engine(config.DB_CONNECTION)
async_session_maker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()
