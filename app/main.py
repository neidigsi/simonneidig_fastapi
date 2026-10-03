"""
FastAPI application entrypoint

Author: Simon Neidig <mail@simon-neidig.eu>

This module creates and configures the FastAPI application instance and includes
all API routers used by the backend. Importing this module prepares the app for
running (e.g. via uvicorn).
"""

# Import external dependencies
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Import internal dependencies
from app.api.routes.contact import contact
from app.api.routes.education import education
from app.api.routes.experience import experience
from app.api.routes.expertise import expertise
from app.api.routes.image import image
from app.api.routes.institution import institution
from app.api.routes.page import page
from app.api.routes.personal_details import personal_details
from app.api.routes.personal_information import personal_information
from app.api.routes.social_media import social_media
from app.api.routes.work import work
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user import auth_backend, fastapi_users


# Initialize FastAPI app
app = FastAPI(
    title="simon-neidig.eu API",
    description="Backend API for simon-neidig.eu, the personal website of Simon Neidig (Freelance Softwareentwickler, Projektleitung & Business Analyse).",
    version="1.0.0",
    contact={
        "name": "Simon Neidig",
        "email": "mail@simon-neidig.eu",
    },
)

# Restrict browser access to the public frontend (plus local dev origins).
# The API itself must never appear in search results (see X-Robots-Tag below).
ALLOWED_ORIGINS = [
    "https://simon-neidig.eu",
    "https://www.simon-neidig.eu",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Attach security headers to every API response.

    X-Robots-Tag `noindex` keeps raw API JSON out of search indexes
    (indexing happens only via the frontend); the frontend `robots.txt`
    additionally disallows crawling `/api/`.
    """
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response

# Define route prefixes as constants
AUTH_PREFIX = "/auth"

# Add routes to FastAPI app
app.include_router(contact.router)
app.include_router(education.router)
app.include_router(experience.router)
app.include_router(expertise.router)
app.include_router(image.router)
app.include_router(institution.router)
app.include_router(page.router)
app.include_router(personal_details.router)
app.include_router(personal_information.router)
app.include_router(social_media.router)
app.include_router(work.router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix=f"{AUTH_PREFIX}/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=AUTH_PREFIX,
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=AUTH_PREFIX,
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix=AUTH_PREFIX,
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)