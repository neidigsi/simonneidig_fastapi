# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import experience as models
from app.db.queries import experience as crud
from app.db.database import engine
from app.schemas import experience as schemas
from app.services.i18n import get_language
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/experience",
    tags=["experience"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Experience])
async def get_experiences(lang: str = Depends(get_language), db: Session = Depends(get_db)):
    return crud.get_experiences(lang, db)
