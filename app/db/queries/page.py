"""
Page query helpers

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides helper functions to load Page objects together with their
localized translation fields (title, abstract, html) for a requested language.
Functions here map translation fields onto Page model instances for API consumption.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.page import Page
from app.db.models.page_translation import PageTranslation
from app.db.models.language import Language


async def get_page(tech_key: str, lang: str, db: AsyncSession):
    """
    Fetch a single Page object by its tech_key with its title, abstract, and HTML
    populated from the corresponding translation for the specified language.

    Args:
        tech_key (str): The technical key of the page.
        lang (str): The language code (e.g., "en", "de").
        db (Session): The database session.

    Returns:
        Page | None: The Page object with translations, or None if not found.
    """
    result = await db.execute(
        select(
            Page,
            PageTranslation.title,
            PageTranslation.abstract,
            PageTranslation.html
        )
        .outerjoin(PageTranslation)
        .where(PageTranslation.language.has(iso639_1=lang))
        .where(Page.tech_key == tech_key)
    )
    
    mapped_result = result.first()
    
    if mapped_result:
        page, title, abstract, html = mapped_result
        page.title = title
        page.abstract = abstract
        page.html = html
        return page

    return None


async def get_pages(lang: str, db: AsyncSession):
    result = await db.execute(
        select(
            Page,
            PageTranslation.title,
            PageTranslation.abstract,
            PageTranslation.html
        )
        .join(PageTranslation)
        .where(PageTranslation.language.has(iso639_1=lang))
    )
    
    pages = result.all()

    # Map the additional fields to the Page object
    mapped_results = []
    for page, title, abstract, html in pages:
        page.title = title
        page.abstract = abstract
        page.html = html
        mapped_results.append(page)  # Append the full Page object

    return mapped_results


async def create_page(lang: str, db: AsyncSession, *, tech_key=None, title=None, abstract=None, html=None, creation_date=None):
    """
    Create a new Page and its localized translation for the given language.

    Returns the newly created Page instance (refreshed).
    """
    # Create the page row
    p = Page(
        tech_key=tech_key, 
        creation_date=creation_date
    )
    
    db.add(p)
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
    translation = PageTranslation(
        title=title,
        abstract=abstract,
        html=html,
        page_id=p.id,
        language_id=language_row.id,
    )
    db.add(translation)

    # Commit both rows
    await db.commit()
    await db.refresh(p)
    
    # Return the full expertise with translations and related objects
    return await get_page(p.tech_key, lang, db)