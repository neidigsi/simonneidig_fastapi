# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import social_media as models
from app.db.queries import social_media as crud
from app.db.database import engine
from app.schemas import social_media as schemass
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/social-media",
    tags=["social media"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.SocialMedia])
async def get_social_medias(db: Session = Depends(get_db)):
    return crud.get_social_medias(db)
