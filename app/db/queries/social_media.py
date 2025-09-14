"""
Social media query helpers

Author: Simon Neidig <mail@simonneidig.de>

Simple query helpers to retrieve social media link records used on the site.
These helpers return SocialMedia model instances for API consumption.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.social_media import SocialMedia

async def get_social_media(social_media_id: int, db: AsyncSession):
    """
    Retrieve a Social Media object by its ID.

    Args:
        social_media_id (int): The ID of the social media object to retrieve.
        db (AsyncSession): SQLAlchemy async database session.

    Returns:
        SocialMedia | None: The SocialMedia instance if found, otherwise None.
    """
    result = await db.execute(select(SocialMedia).where(SocialMedia.id == social_media_id))
    
    social_media = result.first()
    
    if social_media is not None:
        return social_media
    
    return None


async def get_social_medias(db: AsyncSession):
    result = await db.execute(select(SocialMedia))
    
    return result.scalars().all()

async def create_social_media(db: AsyncSession, name=None, url=None, color=None, path=None):
    """
    Create a new Social Media.

    Returns the newly created Social Media instance (refreshed).
    """
    # Create the social media row
    sm = SocialMedia(name=name, url=url, color=color, path=path)
    db.add(sm)
    await db.flush()  # assigns primary key

    # Commit
    await db.commit()
    await db.refresh(sm)
    
    # Return the new instance
    return sm