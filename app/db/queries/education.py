"""
Education query helpers

Author: Simon Neidig <mail@simonneidig.de>

This module provides helper functions to load Education objects together with their
localized translation fields (course_of_study, description) and the localized
institution name for a requested language. Results are mapped onto Education
instances for API consumption.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.education import Education
from app.db.models.education_translation import EducationTranslation
from app.db.models.institution_translation import InstitutionTranslation


def get_educations(lang: str, db: Session):
    educations = db.execute(
        select(
            Education,
            EducationTranslation.course_of_study,
            EducationTranslation.description,
            InstitutionTranslation.name.label("university_name")
        )
        .join(EducationTranslation)
        .join(Education.university)
        .join(InstitutionTranslation, InstitutionTranslation.institution_id == Education.institution_id)
        .where(EducationTranslation.language.has(iso639_1=lang))
        .where(InstitutionTranslation.language.has(iso639_1=lang))
    ).all()

    # Map the additional fields to the Education object
    result = []
    for edu, course_of_study, description, university_name in educations:
        edu.course_of_study = course_of_study
        edu.description = description
        edu.university.name = university_name
        result.append(edu)

    return result
