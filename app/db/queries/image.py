# Import external dependencies
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.image import Image


def get_image(image_id: int, db: Session):
    return db.query(Image).filter(Image.id == image_id).first()
