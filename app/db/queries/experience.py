# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.experience import Experience
from app.db.models.experience_translation import ExperienceTranslation
from app.db.models.institution_translation import InstitutionTranslation


def get_experiences(lang: str, db: Session):
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
