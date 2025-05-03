# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.personal_information import PersonalInformation
from app.db.models.personal_information_translation import PersonalInformationTranslation


def get_personal_information(lang: str, db: Session):
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
