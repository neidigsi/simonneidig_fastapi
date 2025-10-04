"""
Work query helpers

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides helper functions to load Work (portfolio) entries together with
their localized title and associated categories for a requested language. The helper
maps translation fields and localized category names onto Work model instances for
API consumption.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.work import Work
from app.db.models.work_translation import WorkTranslation
from app.db.models.category import Category
from app.db.models.category_translation import CategoryTranslation


async def get_works(lang: str, db: AsyncSession):
    """
    Async helper to retrieve works with localized title and localized category names.

    Args:
        lang (str): Two-letter ISO639-1 language code.
        db (AsyncSession): Async SQLAlchemy session.

    Returns:
        list[Work]: Work instances with `title` and `categories` populated (categories include localized `name`).
    """
    result = await db.execute(
        select(
            Work,
            WorkTranslation.title,
            Category,
            CategoryTranslation.name.label("category_name"),
        )
        .join(WorkTranslation)
        .join(Work.categories)  # join to Category
        .join(
            CategoryTranslation,
            CategoryTranslation.category_id == Category.id,
        )
        .where(WorkTranslation.language.has(iso639_1=lang))
        .where(CategoryTranslation.language.has(iso639_1=lang))
    )

    rows = result.all()

    # Map the additional fields into plain dicts to avoid any lazy-loading on ORM objects
    work_map: dict[int, dict] = {}
    for work, title, category, category_name in rows:
        wid = work.id
        if wid not in work_map:
            work_map[wid] = {
                "id": wid,
                "url": getattr(work, "url", None),
                "thumbnail_id": getattr(work, "thumbnail_id", None) or getattr(work, "thumbnail", None),
                "title": title,
                "categories": [],
            }
        # append localized category name as plain dict (include id to satisfy response schema)
        cat_id = getattr(category, "id", None)
        work_map[wid]["categories"].append({"id": cat_id, "name": category_name})

    # Return a list of plain dicts compatible with the Work Pydantic schema
    return list(work_map.values())
