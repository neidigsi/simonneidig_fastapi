"""
Expertise query helpers

Author: Simon Neidig <mail@simonneidig.de>

This module provides helper functions to load Expertise entries together with
their localized title and description for a requested language. Results are
mapped onto Expertise model instances so they can be returned directly by the API.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.expertise import Expertise
from app.db.models.expertise_translation import ExpertiseTranslation


def get_expertises(lang: str, db: Session):
    """
    Retrieve expertise entries for the given language.

    Args:
        lang (str): Two-letter ISO639-1 language code (e.g. "en", "de", "fr").
        db (Session): SQLAlchemy database session.

    Returns:
        list[Expertise]: List of Expertise objects with `title` and `description`
        attributes populated from the translation table.
    """
    expertises = db.execute(
        select(
            Expertise,
            ExpertiseTranslation.title,
            ExpertiseTranslation.description
        )
        .join(ExpertiseTranslation)
        .where(ExpertiseTranslation.language.has(iso639_1=lang))
    ).all()

    # Map the additional fields to the expertise object
    result = []
    for exp, title, description in expertises:
        exp.title = title
        exp.description = description
        result.append(exp)

    return result
