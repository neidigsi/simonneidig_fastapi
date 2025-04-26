from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.models import education as models
from app.db.queries import education as crud
from app.db.database import SessionLocal, engine
from app.schemas import education as schemas


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/education",
    tags=["education"],
    responses={404: {"description": "Not found"}},
)


def get_language(request: Request):
    lang = request.headers.get("accept-language", "en")
    return lang.split(",")[0].strip().lower()  # z.B. "de-DE,de;q=0.9" -> "de"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.Education])
async def get_education(lang: str = Depends(get_language), db: Session = Depends(get_db)):
    education = crud.get_educations(lang, db)

    return education
