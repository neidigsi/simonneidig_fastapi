# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/{tech_key}", response_model=schemas.Page)
async def get_page(tech_key: str, lang: str = Depends(get_language), db: Session = Depends(get_db)):
    page = crud.get_page(tech_key, lang, db)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page
