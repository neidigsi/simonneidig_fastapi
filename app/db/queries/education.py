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
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.education import Education
from app.db.models.education_translation import EducationTranslation
from app.db.models.institution_translation import InstitutionTranslation
from app.db.models.institution import Institution
from app.db.models.address import Address


async def get_educations(lang: str, db: AsyncSession):
    result = await db.execute(
        select(
            Education,
            EducationTranslation.course_of_study,
            EducationTranslation.description,
            Institution,
            Address,
            InstitutionTranslation.name.label("university_name")
        )
        .join(EducationTranslation)
        .join(Education.university)
        .join(Institution.address) 
        .join(InstitutionTranslation, InstitutionTranslation.institution_id == Education.institution_id)
        .where(EducationTranslation.language.has(iso639_1=lang))
        .where(InstitutionTranslation.language.has(iso639_1=lang))
    )
    
    educations = result.all()
        
    # Map the additional fields to the Eduction object and attach related objects
    mapped_results = []
    for (
        edu,
        course_of_study,
        description,
        university,
        address,
        university_name,
    ) in educations:
        edu.course_of_study = course_of_study
        edu.description = description

        # Attach selected university and address objects to the education instance
        if university is not None:
            # ensure university has the localized name from InstitutionTranslation
            setattr(university, "name", university_name)
            # attach selected address (no IO)
            setattr(university, "address", address)
            # attach university to education (avoid lazy load)
            setattr(edu, "university", university)

        mapped_results.append(edu)

    return mapped_results
