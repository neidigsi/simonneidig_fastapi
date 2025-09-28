"""
Expertise query helpers

Author: Simon Neidig <mail@simonneidig.de>

This module provides helper functions to load Expertise entries together with
their localized title and description for a requested language. Results are
mapped onto Expertise model instances so they can be returned directly by the API.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.expertise import Expertise
from app.db.models.expertise_translation import ExpertiseTranslation
from app.db.models.language import Language


async def get_expertise(expertise_id: int, lang: str, db: AsyncSession):
    """
    Retrieve an Expertise by its ID.

    Args:
        expertise_id (int): The ID of the expertise to retrieve.
        db (AsyncSession): SQLAlchemy async database session.

    Returns:
        Expertise | None: The Expertise instance if found, otherwise None.
    """
    result = await db.execute(
        select(
            Expertise,
            ExpertiseTranslation.title,
            ExpertiseTranslation.description
        )
        .outerjoin(ExpertiseTranslation)
        .where(ExpertiseTranslation.language.has(iso639_1=lang))
        .where(Expertise.id == expertise_id)
    )

    expertise = result.first()

    if expertise is not None:
        (
            exp,
            title,
            description,
        ) = expertise

        exp.title = title
        exp.description = description

        return exp

    return None


async def get_expertises(lang: str, db: AsyncSession):
    """
    Retrieve expertise entries for the given language.

    Args:
        lang (str): Two-letter ISO639-1 language code (e.g. "en", "de", "fr").
        db (Session): SQLAlchemy database session.

    Returns:
        list[Expertise]: List of Expertise objects with `title` and `description`
        attributes populated from the translation table.
    """
    result = await db.execute(
        select(
            Expertise,
            ExpertiseTranslation.title,
            ExpertiseTranslation.description
        )
        .outerjoin(ExpertiseTranslation)
        .where(ExpertiseTranslation.language.has(iso639_1=lang))
    )

    expertises = result.all()

    # Map the additional fields to the expertise object and attach related objects
    mapped_results = []
    for (
        exp,
        title,
        description
    ) in expertises:
        exp.title = title
        exp.description = description

        mapped_results.append(exp)

    return mapped_results


async def create_expertise(lang: str, db: AsyncSession, *, title=None, description=None, icon=None, sort=None):
    """
    Create a new Expertise and its localized translation for the given language.

    Returns the newly created Expertise instance (refreshed).
    """
    # Create the experience row
    exp = Expertise(
        icon=icon, 
        sort=sort
    )
    
    db.add(exp)
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
    translation = ExpertiseTranslation(
        title=title,
        description=description,
        expertise_id=exp.id,
        language_id=language_row.id,
    )
    db.add(translation)

    # Commit both rows
    await db.commit()
    await db.refresh(exp)
    
    # Return the full expertise with translations and related objects
    return await get_expertise(exp.id, lang, db)