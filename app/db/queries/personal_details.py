"""
Personal details query helpers

Author: Simon Neidig <mail@simonneidig.de>

This module provides a helper to load the primary PersonalDetails record together
with its localized fields (position, abstract) for a requested language.
The function maps translation fields onto the PersonalDetails model instance
so the returned object can be directly consumed by the API layer.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.personal_details import PersonalDetails
from app.db.models.personal_details_translation import PersonalDetailsTranslation


def get_personal_details(lang: str, db: Session):
    """
    Fetch the first PersonalDetails object with its position and abstract
    populated from the corresponding translation for the specified language.

    Args:
        lang (str): The language code (e.g., "en", "de").
        db (Session): The database session.

    Returns:
        PersonalDetails | None: The first PersonalDetails object with translations, or None if not found.
    """
    result = db.execute(
        select(
            PersonalDetails,
            PersonalDetailsTranslation.position,
            PersonalDetailsTranslation.abstract
        )
        .join(PersonalDetailsTranslation)
        .where(PersonalDetailsTranslation.language.has(iso639_1=lang))
    ).first()

    if result:
        personal_details, position, abstract = result
        personal_details.position = position
        personal_details.abstract = abstract
        return personal_details

    return None

