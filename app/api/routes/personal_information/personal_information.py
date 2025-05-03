# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import personal_information as models
from app.db.queries import personal_information as crud
from app.db.database import engine
from app.schemas import personal_information as schemas
from app.services.i18n import get_language
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/personal-information",
    tags=["personal-information"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.PersonalInformation])
async def get_personal_information(lang: str = Depends(get_language), db: Session = Depends(get_db)):
    return crud.get_personal_information(lang, db)
