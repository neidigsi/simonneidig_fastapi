"""
Education API routes.

Provides endpoints to list and create 'Education' entries.

Author: Simon Neidig <mail@simon-neidig.eu>

- GET /education/  -> List education entries for a requested language.
- POST /education/ -> Create a new education entry (requires superuser).

Notes:
- Language is resolved via the `get_language` dependency.
- Database access is provided via an AsyncSession from `get_async_session`.
- Authorization for creating entries is enforced via fastapi-users (superuser).
"""

# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.queries import education as crud
from app.schemas import education as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session
from app.services.user import fastapi_users


# dependency that enforces the current user to be a superuser
get_current_superuser = fastapi_users.current_user(superuser=True)


# Create a new APIRouter instance for the education API
router = APIRouter(
    prefix="/education",
    tags=["education"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.EducationRead])
async def get_education(lang: str = Depends(get_language), db: AsyncSession = Depends(get_async_session)):
    """
    Retrieve education entries.

    Args:
        lang (str): Language code resolved by the get_language dependency (e.g. 'en', 'de', 'fr').
        db (AsyncSession): Async SQLAlchemy session provided by dependency injection.

    Returns:
        list[EducationRead]: A list of education items serialized with the EducationRead schema.

    Notes:
        - This endpoint is read-only and publicly accessible.
        - Pagination and filtering are not implemented here (can be added later if needed).
    """
    return await crud.get_educations(lang, db)



@router.post("/", response_model=schemas.EducationRead, status_code=status.HTTP_201_CREATED)
async def create_education(
    payload: schemas.EducationCreate,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_async_session),
    _admin=Depends(get_current_superuser),
    response: Response = None,
):
    """
    Create a new education entry (admin only).

    Args:
        payload (EducationCreate): Payload validated against the EducationCreate schema.
        lang (str): Language code for the content to be created.
        db (AsyncSession): Async database session.
        _admin: Injected current user (must be superuser) — used for authorization only.
        response (Response): FastAPI Response object used to set headers.

    Returns:
        EducationRead: The created education object serialized with the EducationRead schema.

    Raises:
        HTTPException(500): If creation failed for any reason.

    Notes:
        - On success, the response will include the 'Content-Language' header set to the requested language.
    """
    edu = await crud.create_education(
        lang,
        db,
        start_date=payload.start_date,
        end_date=payload.end_date,
        degree=payload.degree,
        grade=payload.grade,
        institution_id=payload.institution_id,
        course_of_study=payload.course_of_study,
        description=payload.description,
    )
    
    if not edu:
        raise HTTPException(status_code=500, detail="Failed to create education")
    
    # set the language in the response headers so clients can easily detect the content language
    if response is not None:
        response.headers["Content-Language"] = lang
    
    return edu
