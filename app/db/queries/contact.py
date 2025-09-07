"""
Contact queries for the database

Author: Simon Neidig <mail@simonneidig.de>

This module contains database query helpers related to contact inquiries submitted via the website.
A "Contact" represents a message submitted through the site's contact form; these helpers
handle persisting such inquiries and associating them with a language record.

Main features:
- Persist contact inquiries to the database.
- Resolve and validate language association by ISO639-1 code.
- Provide a simple, reusable API for other services/routes to save contact messages.
"""

# Import external dependencies
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

# Import internal dependencies
from app.db.models.contact import Contact
from app.schemas.contact import SendingContact
from app.db.models.language import Language  # Import the Language model

async def save_contact(contact: SendingContact, db: AsyncSession, lang: str) -> Contact:
    """
    Save a new contact to the database (async).

    Args:
        contact (SendingContact): The contact data to save.
        db (AsyncSession): The async database session.
        lang (str): The language code to associate with the contact.

    Returns:
        Contact: The saved contact object.
    """
    # Fetch the language object based on the provided language code (async)
    result = await db.execute(select(Language).where(Language.iso639_1 == lang))
    language = result.scalar_one_or_none()

    if not language:
        raise ValueError(f"Language '{lang}' not found in the database.")

    try:
        # Use a naive UTC datetime because the DB column is TIMESTAMP WITHOUT TIME ZONE.
        # Creating an aware datetime (with tzinfo) causes asyncpg/DataError when inserting.
        naive_utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
        new_contact = Contact(
            name=contact.name,
            email=contact.email,
            message=contact.message,
            creation_date=naive_utc_now,
            sended=False,
            language_id=language.id
        )
        db.add(new_contact)
        await db.commit()
        await db.refresh(new_contact)
        return new_contact
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Validation or DB error: {e}")

