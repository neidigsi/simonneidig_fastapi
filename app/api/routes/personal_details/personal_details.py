# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import personal_details as models
from app.db.queries import personal_details as crud
from app.db.database import engine
from app.schemas import personal_details as schemas
from app.services.i18n import get_language
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/personal-details",
    tags=["personal-details"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.PersonalDetails)
async def get_personal_details(lang: str = Depends(get_language), db: Session = Depends(get_db)):
    personal_details = crud.get_personal_details(lang, db)
    if not personal_details:
        raise HTTPException(status_code=404, detail="Personal details not found")
    return personal_details
