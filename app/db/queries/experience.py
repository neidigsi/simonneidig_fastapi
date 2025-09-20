"""
Experience query helpers (async)

Author: Simon Neidig <mail@simonneidig.de>

This module provides helpers to load Experience entries together with their
localized title, extract, description, industry and associated company name
for a requested language. Results are mapped onto Experience model instances
so they can be returned directly by the API.
"""

# Import external dependencies
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.experience import Experience
from app.db.models.experience_translation import ExperienceTranslation
from app.db.models.institution_translation import InstitutionTranslation
from app.db.models.institution import Institution
from app.db.models.address import Address
from app.db.models.language import Language

async def get_experience(experience_id: int, lang: str, db: AsyncSession):
    """
    Retrieve an Experience by its ID.

    Args:
        experience_id (int): The ID of the experience to retrieve.
        db (AsyncSession): SQLAlchemy async database session.

    Returns:
        Experience | None: The Experience instance if found, otherwise None.
    """
    result = await db.execute(
        select(
            Experience,
            ExperienceTranslation.title,
            ExperienceTranslation.extract,
            ExperienceTranslation.description,
            ExperienceTranslation.industry,
            Institution,
            Address,
            InstitutionTranslation.name.label("company_name"),
        )
        .outerjoin(ExperienceTranslation)
        .outerjoin(Experience.company)
        .outerjoin(Institution.address) 
        .outerjoin(InstitutionTranslation, InstitutionTranslation.institution_id == Experience.institution_id)
        .where(ExperienceTranslation.language.has(iso639_1=lang))
        .where(
            or_(
                InstitutionTranslation.language.has(iso639_1=lang),
                Institution.id == None,
            )
        )
        .where(Experience.id == experience_id)
    )

    experience = result.first()

    if experience is not None:
        (
           exp,
        title,
        extract,
        description,
        industry,
        company,
        address,
        company_name,
        ) = experience

        exp.title = title
        exp.extract = extract
        exp.description = description
        exp.industry = industry

        # Attach selected company and address objects to the experience instance
        if company is not None:
            # ensure company has the localized name from InstitutionTranslation
            setattr(company, "name", company_name)
            # attach selected address (no IO)
            setattr(company, "address", address)
            # attach company to experience (avoid lazy load)
            setattr(exp, "company", company)

        return exp
    
    return None


async def get_experiences(lang: str, db: AsyncSession):
    """
    Retrieve experience entries for the given language.

    Args:
        lang (str): Two-letter ISO639-1 language code (e.g. "en", "de", "fr").
        db (AsyncSession): SQLAlchemy async database session.

    Returns:
        list[Experience]: List of Experience objects with translation fields (title, extract,
        description, industry) and the associated company's name and address populated
        from translation tables. Related objects are selected eagerly to avoid lazy I/O.
    """
    result = await db.execute(
        select(
            Experience,
            ExperienceTranslation.title,
            ExperienceTranslation.extract,
            ExperienceTranslation.description,
            ExperienceTranslation.industry,
            Institution,
            Address,
            InstitutionTranslation.name.label("company_name"),
        )
        .outerjoin(ExperienceTranslation)
        .outerjoin(Experience.company)
        .outerjoin(Institution.address) 
        .outerjoin(InstitutionTranslation, InstitutionTranslation.institution_id == Experience.institution_id)
        .where(ExperienceTranslation.language.has(iso639_1=lang))
        .where(
            or_(
                InstitutionTranslation.language.has(iso639_1=lang),
                Institution.id == None,
            )
        )
    )

    experiences = result.all()

    # Map the additional fields to the Experience object and attach related objects
    mapped_results = []
    for (
        exp,
        title,
        extract,
        description,
        industry,
        company,
        address,
        company_name,
    ) in experiences:
        exp.title = title
        exp.extract = extract
        exp.description = description
        exp.industry = industry

        # Attach selected company and address objects to the experience instance
        if company is not None:
            # ensure company has the localized name from InstitutionTranslation
            setattr(company, "name", company_name)
            # attach selected address (no IO)
            setattr(company, "address", address)
            # attach company to experience (avoid lazy load)
            setattr(exp, "company", company)

        mapped_results.append(exp)

    return mapped_results


async def create_experience(lang: str, db: AsyncSession, *,
                            title=None, extract=None, description=None, industry=None, url=None,
                           start_date=None, end_date=None, institution_id=None):
    """
    Create a new Experience and its localized translation for the given language.

    Returns the newly created Experience instance (refreshed).
    """
    # Create the experience row
    exp = Experience(
        url=url, 
        start_date=start_date, 
        end_date=end_date, 
        institution_id=institution_id
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
    translation = ExperienceTranslation(
        title=title,
        extract=extract,
        description=description,
        industry=industry,
        experience_id=exp.id,
        language_id=language_row.id,
    )
    db.add(translation)

    # Commit both rows
    await db.commit()
    await db.refresh(exp)
    
    # Return the full experience with translations and related objects
    return await get_experience(exp.id, lang, db)