"""
Work query helpers

Author: Simon Neidig <mail@simonneidig.de>

This module provides helper functions to load Work (portfolio) entries together with
their localized title and associated categories for a requested language. The helper
maps translation fields and localized category names onto Work model instances for
API consumption.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.work import Work
from app.db.models.work_translation import WorkTranslation
from app.db.models.category import Category
from app.db.models.category_translation import CategoryTranslation

def get_works(lang: str, db: Session):
    works = db.execute(
        select(
            Work,
            WorkTranslation.title,
            Category,
            CategoryTranslation.name
        )
        .join(WorkTranslation)
        .join(Work.categories)  # Assuming Work has a relationship to Category
        .join(CategoryTranslation)
        .where(WorkTranslation.language.has(iso639_1=lang))
        .where(CategoryTranslation.language.has(iso639_1=lang))
    ).all()

    # Map the additional fields to the work object
    work_map = {}
    for work, title, category, category_name in works:
        if work.id not in work_map:
            work.title = title
            work.categories = []
            work_map[work.id] = work
        category.name = category_name
        work_map[work.id].categories.append(category)

    return list(work_map.values())
