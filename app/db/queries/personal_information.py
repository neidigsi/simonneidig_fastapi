"""
Personal information query helpers

Author: Simon Neidig <mail@simonneidig.de>

This module provides helpers to load short personal information items (label/value)
for the requested language. Each returned PersonalInformation model instance will
have its localized label and value mapped onto the object for API consumption.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.personal_information import PersonalInformation
from app.db.models.personal_information_translation import PersonalInformationTranslation


def get_personal_information(lang: str, db: Session):
    """
    Retrieve personal information entries for a given language.

    Args:
        lang (str): Two-letter ISO639-1 language code (e.g. "en", "de", "fr").
        db (Session): SQLAlchemy database session.

    Returns:
        list[PersonalInformation]: List of PersonalInformation objects with
        `label` and `value` attributes populated from the translation table.
    """
    personal_information = db.execute(
        select(
            PersonalInformation,
            PersonalInformationTranslation.label,
            PersonalInformationTranslation.value
        )
        .join(PersonalInformationTranslation)
        .where(PersonalInformationTranslation.language.has(iso639_1=lang))
    ).all()

    # Map the additional fields to the personal information object
    result = []
    for info, label, value in personal_information:
        info.label = label
        info.value = value
        result.append(info)
    
    return result
