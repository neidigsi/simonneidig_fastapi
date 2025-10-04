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
        .join(PageTranslation)
        .where(Page.tech_key == tech_key)
        .where(PageTranslation.language.has(iso639_1=lang))
    )
    
    mapped_result = result.first()
    
    if mapped_result:
        page, title, abstract, html = mapped_result
        page.title = title
        page.abstract = abstract
        page.html = html
        return page

    return None
