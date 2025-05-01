# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.expertise import Expertise
from app.db.models.expertise_translation import ExpertiseTranslation


def get_expertises(lang: str, db: Session):
    expertises = db.execute(
        select(
            Expertise,
            ExpertiseTranslation.title,
            ExpertiseTranslation.description
        )
        .join(ExpertiseTranslation)
        .where(ExpertiseTranslation.language.has(iso639_1=lang))
    ).all()

    # Map the additional fields to the Experience object
    result = []
    for exp, title, description in expertises:
        exp.title = title
        exp.description = description
        result.append(exp)

    return result
