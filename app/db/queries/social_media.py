"""
Social media query helpers

Author: Simon Neidig <mail@simonneidig.de>

Simple query helpers to retrieve social media link records used on the site.
These helpers return SocialMedia model instances for API consumption.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.social_media import SocialMedia


def get_social_medias(db: Session):
    return db.execute(
        select(SocialMedia)
    ).scalars().all()
