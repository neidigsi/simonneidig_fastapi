"""
User service and FastAPI Users integration.

Provides user management integration for the application using fastapi-users.
This module defines:
- a UserManager implementing lifecycle hooks (register, password reset, verification),
- factory helpers for dependency injection,
- the FastAPIUsers instance and authentication backend configuration.

Author: Simon Neidig <mail@simon-neidig.eu>
"""

# Import external dependencies
import uuid
import os
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import ( BaseUserManager, FastAPIUsers, UUIDIDMixin )
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)


# Import internal dependencies
from app.services.db import User, get_user_db

SECRET = os.getenv('SECRET_KEY')


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """
    Application-specific user manager.

    Implements hooks that are executed after user registration, password reset
    requests and email verification requests. Hooks currently log events to stdout;
    extend these methods to integrate with notification systems or analytics.

    Note: secrets for tokens are read from the SECRET_KEY environment variable.
    """

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    """
    Dependency factory that yields a UserManager instance.

    Args:
        user_db: SQLAlchemyUserDatabase provided by get_user_db dependency.

    Yields:
        UserManager instance configured with the provided user_db.
    """
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
