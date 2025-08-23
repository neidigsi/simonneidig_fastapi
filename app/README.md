# Application

This document provides an overview of the application's structure.  
It is intended to help developers quickly understand the organization of the codebase and the purpose of each main directory.  
By following these guidelines, contributors can efficiently navigate, maintain, and extend the project.

## Code Structure

The codebase is organized into several main directories, each serving a specific purpose to ensure maintainability, scalability, and clarity:

- **api/** – Contains FastAPI route implementations and routers that define the HTTP endpoints of the application.
  
- **core/** – Holds application-wide configuration, constants, and startup utilities (such as config loading and logging).
  
- **db/** – Includes the database layer: SQLAlchemy models, Alembic migrations, and query helpers for data access.
  
- **resources/** – Stores static assets and ancillary resources used by the application (such as media, templates, or static files).
  
- **schemas/** – Defines Pydantic schemas for request validation and response serialization across the API.
  
- **services/** – Implements business logic and higher-level application services that coordinate queries, models, and external integrations.

This modular structure allows for clear separation of concerns, making it easy to locate, maintain, and extend functionality as the application grows.