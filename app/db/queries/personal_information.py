"""
Personal information query helpers

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides helpers to load short personal information items (label/value)
for the requested language. Each returned PersonalInformation model instance will
have its localized label and value mapped onto the object for API consumption.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.personal_information import PersonalInformation
from app.db.models.personal_information_translation import PersonalInformationTranslation
from app.db.models.language import Language


async def get_single_personal_information(personal_information_id: int, lang: str, db: AsyncSession):
    """
    Retrieve a single personal information entry for a given language.

    Args:
        lang (str): Two-letter ISO639-1 language code (e.g. "en", "de", "fr").
        db (Session): SQLAlchemy database session.

    Returns:
        PersonalInformation: The PersonalInformation object with
        `label` and `value` attributes populated from the translation table.
    """
    result = await db.execute(
        select(
            PersonalInformation,
            PersonalInformationTranslation.label,
            PersonalInformationTranslation.value
        )
        .outerjoin(PersonalInformationTranslation)
        .where(PersonalInformationTranslation.language.has(iso639_1=lang))
        .where(PersonalInformation.id == personal_information_id)
    )

    personal_information = result.first()

    if personal_information is not None:
        (
            info,
            label,
            value
        ) = personal_information
        info.label = label
        info.value = value
        
        return info

    return None


async def get_personal_information(lang: str, db: AsyncSession):
    """
    Retrieve personal information entries for a given language.

    Args:
        lang (str): Two-letter ISO639-1 language code (e.g. "en", "de", "fr").
        db (Session): SQLAlchemy database session.

    Returns:
        list[PersonalInformation]: List of PersonalInformation objects with
        `label` and `value` attributes populated from the translation table.
    """
    result = await db.execute(
        select(
            PersonalInformation,
            PersonalInformationTranslation.label,
            PersonalInformationTranslation.value
        )
        .outerjoin(PersonalInformationTranslation)
        .where(PersonalInformationTranslation.language.has(iso639_1=lang))
    )

    personal_information = result.all()

    # Map the additional fields to the personal information object
    mapped_results = []
    for info, label, value in personal_information:
        info.label = label
        info.value = value
        mapped_results.append(info)

    return mapped_results


async def create_personal_information(lang: str, db: AsyncSession, *, label=None, value=None, icon=None):
    """
    Create a new Expertise and its localized translation for the given language.

    Returns the newly created Expertise instance (refreshed).
    """
    # Create the personal information row
    pi = PersonalInformation(
        icon=icon
    )
    
    db.add(pi)
    await db.flush()  # assigns primary key

    # Find language id
    result = await db.execute(
        select(Language).where(Language.iso639_1 == lang)
    )
    language_row = result.scalars().first()

    if language_row is None:
        # Create a language fallback if not present
        language_row = Language(name=lang, iso639_1=lang)
        db.add(language_row)
        await db.flush()

    # Create translation
    translation = PersonalInformationTranslation(
        label=label,
        value=value,
        personal_information_id=pi.id,
        language_id=language_row.id,
    )
    db.add(translation)

    # Commit both rows
    await db.commit()
    await db.refresh(pi)
    
    # Return the full personal information with translations and related objects
    return await get_single_personal_information(pi.id, lang, db)