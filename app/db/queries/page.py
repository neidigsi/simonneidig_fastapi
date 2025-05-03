# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.page import Page
from app.db.models.page_translation import PageTranslation


def get_pages(lang: str, db: Session):
    pages = db.execute(
        select(
            Page,
            PageTranslation.title,
            PageTranslation.abstract,
            PageTranslation.html
        )
        .join(PageTranslation)
        .where(PageTranslation.language.has(iso639_1=lang))
    ).all()

    # Map the additional fields to the Page object
    result = []
    for page, title, abstract, html in pages:
        page.title = title
        page.abstract = abstract
        page.html = html
        result.append(page)  # Append the full Page object

    return result


def get_page(tech_key: str, lang: str, db: Session):
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
    result = db.execute(
        select(
            Page,
            PageTranslation.title,
            PageTranslation.abstract,
            PageTranslation.html
        )
        .join(PageTranslation)
        .where(Page.tech_key == tech_key)
        .where(PageTranslation.language.has(iso639_1=lang))
    ).first()

    if result:
        page, title, abstract, html = result
        page.title = title
        page.abstract = abstract
        page.html = html
        return page

    return None
