# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.social_media import SocialMedia


def get_social_medias(db: Session):
    return db.execute(
        select(SocialMedia)
    ).scalars().all()
