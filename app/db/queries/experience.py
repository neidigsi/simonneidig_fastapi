"""
Experience query helpers

Author: Simon Neidig <mail@simonneidig.de>

This module provides helpers to load Experience entries together with their
localized title, extract, description, industry and associated company name
for a requested language. Results are mapped onto Experience model instances
so they can be returned directly by the API.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.experience import Experience
from app.db.models.experience_translation import ExperienceTranslation
from app.db.models.institution_translation import InstitutionTranslation


def get_experiences(lang: str, db: Session):
    """
    Retrieve experience entries for the given language.

    Args:
        lang (str): Two-letter ISO639-1 language code (e.g. "en", "de", "fr").
        db (Session): SQLAlchemy database session.

    Returns:
        list[Experience]: List of Experience objects with translation fields (title, extract,
        description, industry) and the associated company's name populated from translation tables.
    """
    experiences = db.execute(
        select(
            Experience,
            ExperienceTranslation.title,
            ExperienceTranslation.extract,
            ExperienceTranslation.description,
            ExperienceTranslation.industry,
            InstitutionTranslation.name.label("company_name")
        )
        .join(ExperienceTranslation)
        .join(Experience.company)
        .join(InstitutionTranslation, InstitutionTranslation.institution_id == Experience.institution_id)
        .where(ExperienceTranslation.language.has(iso639_1=lang))
        .where(InstitutionTranslation.language.has(iso639_1=lang))
    ).all()

    # Map the additional fields to the Experience object
    result = []
    for exp, title, extract, description, industry, company_name in experiences:
        exp.title = title
        exp.extract = extract
        exp.description = description
        exp.industry = industry
        exp.company.name = company_name
        result.append(exp)

    return result
