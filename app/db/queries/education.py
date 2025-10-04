"""
Education query helpers

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides helper functions to load Education objects together with their
localized translation fields (course_of_study, description) and the localized
institution name for a requested language. Results are mapped onto Education
instances for API consumption.
"""

# Import external dependencies
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.education import Education
from app.db.models.education_translation import EducationTranslation
from app.db.models.institution_translation import InstitutionTranslation
from app.db.models.institution import Institution
from app.db.models.address import Address
from app.db.models.language import Language


async def get_education(education_id: int, lang: str, db: AsyncSession):
    """
    Retrieve an Education by its ID.

    Args:
        education_id (int): The ID of the education to retrieve.
        db (AsyncSession): SQLAlchemy async database session.

    Returns:
        Education | None: The Education instance if found, otherwise None.
    """
    result = await db.execute(
        select(
            Education,
            EducationTranslation.course_of_study,
            EducationTranslation.description,
            Institution,
            Address,
            InstitutionTranslation.name.label("university_name")
        )
        .outerjoin(EducationTranslation)
        .outerjoin(Education.university)
        .outerjoin(Institution.address) 
        .outerjoin(InstitutionTranslation, InstitutionTranslation.institution_id == Education.institution_id)
        .where(EducationTranslation.language.has(iso639_1=lang))
        .where(
            or_(
                InstitutionTranslation.language.has(iso639_1=lang),
                Institution.id == None,
            )
        )
        .where(Education.id == education_id)
    )    
    
    education = result.first()
    
    if education is not None:
        (
            edu,
            course_of_study,
            description,
            university,
            address,
            university_name,
        ) = education

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

        return edu
    
    return None


async def get_educations(lang: str, db: AsyncSession):
    """
    Retrieve education entries for the given language.

    Args:
        lang (str): Two-letter ISO639-1 language code (e.g. "en", "de", "fr").
        db (AsyncSession): SQLAlchemy async database session.

    Returns:
        list[Education]: List of Education objects with translation fields and the associated 
        university's name and address populated from translation tables.
        Related objects are selected eagerly to avoid lazy I/O.
    """
    
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
        .outerjoin(Education.university)
        .outerjoin(Institution.address)
        .outerjoin(InstitutionTranslation, InstitutionTranslation.institution_id == Education.institution_id)
        .where(EducationTranslation.language.has(iso639_1=lang))
        .where(
            or_(
                InstitutionTranslation.language.has(iso639_1=lang),
                Institution.id == None,
            )
        )
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


async def create_education(lang: str, db: AsyncSession, *,
                           start_date=None, end_date=None, degree=None, grade=None,
                           institution_id=None, course_of_study=None, description=None):
    """
    Create a new Education and its localized translation for the given language.

    Returns the newly created Education instance (refreshed).
    """
    # Create the education row
    edu = Education(
        start_date=start_date,
        end_date=end_date,
        degree=degree, 
        grade=grade,
        institution_id=institution_id
    )
    
    db.add(edu)
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
    translation = EducationTranslation(
        course_of_study=course_of_study,
        description=description,
        education_id=edu.id,
        language_id=language_row.id,
    )
    db.add(translation)

    # Commit both rows
    await db.commit()
    await db.refresh(edu)
    
    # Return the full education with translations and related objects
    return await get_education(edu.id, lang, db)