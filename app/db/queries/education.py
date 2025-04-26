from sqlalchemy.orm import Session

from app.db.models import education as models


def get_educations(lang: str, db: Session):
    
    return db.query(models.Education)
