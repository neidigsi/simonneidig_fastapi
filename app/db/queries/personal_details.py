"""
Personal details query helpers

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides a helper to load the primary PersonalDetails record together
with its localized fields (position, abstract) for a requested language.
The function maps translation fields onto the PersonalDetails model instance
so the returned object can be directly consumed by the API layer.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.personal_details import PersonalDetails
from app.db.models.personal_details_translation import PersonalDetailsTranslation


async def get_personal_details(lang: str, db: AsyncSession):
    """
    Fetch the first PersonalDetails object with its position and abstract
    populated from the corresponding translation for the specified language.

    Args:
        lang (str): The language code (e.g., "en", "de").
        db (AsyncSession): The async SQLAlchemy session.

    Returns:
        PersonalDetails | None: The first PersonalDetails object with translations, or None if not found.
    """
    result = await db.execute(
        select(
            PersonalDetails,
            PersonalDetailsTranslation.position,
            PersonalDetailsTranslation.abstract,
        )
        .join(PersonalDetailsTranslation)
        .where(PersonalDetailsTranslation.language.has(iso639_1=lang))
    )

    row = result.first()
    if row:
        personal_details, position, abstract = row
        personal_details.position = position
        personal_details.abstract = abstract
        return personal_details

    return None

