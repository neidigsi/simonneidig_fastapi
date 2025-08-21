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
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Import internal dependencies
from app.core import config


# Create database engine and connect to configured db string
engine = create_engine(config.DB_CONNECTION)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
