# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import page as models
from app.db.queries import page as crud
from app.db.database import engine
from app.schemas import page as schemas
from app.services.i18n import get_language
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/page",
    tags=["page"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Page])
async def get_pages(lang: str = Depends(get_language), db: Session = Depends(get_db)):
    return crud.get_pages(lang, db)
