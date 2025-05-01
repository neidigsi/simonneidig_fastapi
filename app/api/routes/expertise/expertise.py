# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import expertise as models
from app.db.queries import expertise as crud
from app.db.database import engine
from app.schemas import expertise as schemas
from app.services.i18n import get_language
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/expertise",
    tags=["expertise"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Expertise])
async def get_expertises(lang: str = Depends(get_language), db: Session = Depends(get_db)):
    return crud.get_expertises(lang, db)
