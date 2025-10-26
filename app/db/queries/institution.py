"""
Institution query helpers

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides helper functions to load Institution entries together with
their localized name for a requested language. Results are
mapped onto Institution model instances so they can be returned directly by the API.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.institution import Institution
from app.db.models.address import Address
from app.db.models.institution_translation import InstitutionTranslation
from app.db.models.language import Language


async def get_institution(institution_id: int, lang: str, db: AsyncSession):
    """
    Retrieve an Institution by its ID.

    Args:
        institution_id (int): The ID of the institution to retrieve.
        db (AsyncSession): SQLAlchemy async database session.

    Returns:
        Institution | None: The Institution instance if found, otherwise None.
    """
    result = await db.execute(
        select(
            Institution,
            InstitutionTranslation.name,
            Address
        )
        .outerjoin(InstitutionTranslation)
        .outerjoin(Address)
        .where(InstitutionTranslation.language.has(iso639_1=lang))
        .where(Institution.id == institution_id)
    )

    institution = result.first()

    if institution is not None:
        (
            inst,
            name,
            address,
        ) = institution

        inst.name = name
        inst.address = address

        return inst

    return None


async def get_institutions(lang: str, db: AsyncSession):
    """
    Retrieve institution entries for the given language.

    Args:
        lang (str): Two-letter ISO639-1 language code (e.g. "en", "de", "fr").
        db (Session): SQLAlchemy database session.

    Returns:
        list[Institution]: List of Institution objects with `name`
        attributes populated from the translation table.
    """
    result = await db.execute(
        select(
            Institution,
            InstitutionTranslation.name,
            Address
        )
        .outerjoin(InstitutionTranslation)
        .outerjoin(Address)
        .where(InstitutionTranslation.language.has(iso639_1=lang))
    )

    institutions = result.all()

    # Map the additional fields to the institution object and attach related objects
    mapped_results = []
    for (
        inst,
        name,
        address,
    ) in institutions:
        inst.name = name
        inst.address = address
        
        mapped_results.append(inst)

    return mapped_results


async def create_institution(lang: str, db: AsyncSession, *, name=None, address_id=None):
    """
    Create a new Institution and its localized translation for the given language.

    Returns the newly created Institution instance (refreshed).
    """
    # Create the institution row
    inst = Institution(
        address_id=address_id
    )
    
    db.add(inst)
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
    translation = InstitutionTranslation(
        name=name,
        institution_id=inst.id,
        language_id=language_row.id,
    )
    db.add(translation)

    # Commit both rows
    await db.commit()
    await db.refresh(inst)
    
    # Return the full institution with translations and related objects
    return await get_institution(inst.id, lang, db)