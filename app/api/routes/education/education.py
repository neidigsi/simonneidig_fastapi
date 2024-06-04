from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import education as models
from app.db.schemas import education as schemas
from app.db.queries import education as crud
from app.db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/education",
    tags=["education"],
    responses={404: {"description": "Not found"}},
)

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.Education])
async def get_education(db: Session = Depends(get_db)):
    education = crud.get_educations(db)

    return education
