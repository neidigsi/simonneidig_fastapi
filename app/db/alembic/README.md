# Migrations

Managing changes to the database schema is an essential part of database management in any project. It is important to ensure that migrations are robust and error-resistant. In this project, migration management is handled using [Alembic](https://alembic.sqlalchemy.org/en/latest/).

## Creating Migrations

Database changes, also known as migrations, can be created easily with the following command:

```
alembic revision --autogenerate -m "Change message"
```

It is recommended to provide a meaningful change message that clearly describes the purpose of the migration.

## Applying Migrations

Outstanding migrations can be applied to the database using the following command:

```
alembic upgrade head
```

This command applies the changes to the database connection specified in the `env.py` file within the Alembic directory. You can check the current state of the database by looking at the `alembic_version` table, which records the latest applied migration.