# SQLAlchemy Database Models

This directory contains all database model definitions for the application. Models are implemented using SQLAlchemy](https://www.sqlalchemy.org) and serve as the canonical representation of persisted data used across the backend. Each model defines a table and includes a unique integer identifier named `id` that acts as the primary key.

## Translation Strategy

Models that contain text fields intended for localization follow a translation pattern: each such entity has a one-to-many relationship to a dedicated translation table whose name ends with the `_translation` suffix. Translation rows include a foreign key to the `language` table so that text-based attributes can be provided in different languages.

## Database Access

This directory only defines schema and relationships. Actual data access and query logic are implemented in helper modules under [../queries](../queries/). Those query helpers perform the necessary joins with translation tables and return locale-aware model instances for use by the API layer.