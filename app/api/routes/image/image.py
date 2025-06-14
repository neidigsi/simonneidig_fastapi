

# Import external dependencies
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import image as models
from app.db.queries import image as crud
from app.db.database import engine
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{image_id}", response_class=FileResponse)
def get_image(image_id: int, db: Session = Depends(get_db)):
    image = crud.get_image(image_id, db)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    if not os.path.exists(image.filepath):
        raise HTTPException(
            status_code=404, detail="Image file missing on disk")

    # oder image/png
    return FileResponse(image.filepath, media_type="image/jpeg")
