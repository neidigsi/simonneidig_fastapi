"""
FastAPI application entrypoint

Author: Simon Neidig <mail@simonneidig.de>

This module creates and configures the FastAPI application instance and includes
all API routers used by the backend. Importing this module prepares the app for
running (e.g. via uvicorn).
"""

# Import external dependencies
from fastapi import FastAPI

# Import internal dependencies
from app.api.routes.contact import contact
from app.api.routes.education import education
from app.api.routes.experience import experience
from app.api.routes.expertise import expertise
from app.api.routes.image import image
from app.api.routes.page import page
from app.api.routes.personal_details import personal_details
from app.api.routes.personal_information import personal_information
from app.api.routes.social_media import social_media
from app.api.routes.work import work
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user import auth_backend, current_active_user, fastapi_users


# Initialize FastAPI app
app = FastAPI()

# Add routes to FastAPI app
app.include_router(contact.router)
app.include_router(education.router)
app.include_router(experience.router)
app.include_router(expertise.router)
app.include_router(image.router)
app.include_router(page.router)
app.include_router(personal_details.router)
app.include_router(personal_information.router)
app.include_router(social_media.router)
app.include_router(work.router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)