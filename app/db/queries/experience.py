"""
Experience query helpers (async)

Author: Simon Neidig <mail@simonneidig.de>

This module provides helpers to load Experience entries together with their
localized title, extract, description, industry and associated company name
for a requested language. Results are mapped onto Experience model instances
so they can be returned directly by the API.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.experience import Experience
from app.db.models.experience_translation import ExperienceTranslation
from app.db.models.institution_translation import InstitutionTranslation
from app.db.models.institution import Institution
from app.db.models.address import Address


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
        .join(ExperienceTranslation)
        .join(Experience.company)          # join to Institution
        .join(Institution.address)         # join to Address
        .join(
            InstitutionTranslation,
            InstitutionTranslation.institution_id == Experience.institution_id,
        )
        .where(ExperienceTranslation.language.has(iso639_1=lang))
        .where(InstitutionTranslation.language.has(iso639_1=lang))
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
