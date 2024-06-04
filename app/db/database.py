# Import external dependencies
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import internal dependencies
from app.core import config


# Create database engine and connect to configured db string
engine = create_engine(config.DB_CONNECTION)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
