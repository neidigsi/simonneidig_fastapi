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
from pydantic import ValidationError
from sqlalchemy.orm import Session
from datetime import datetime, timezone

# Import internal dependencies
from app.db.models.contact import Contact
from app.schemas.contact import SendingContact
from app.db.models.language import Language  # Import the Language model

def save_contact(contact: SendingContact, db: Session, lang: str) -> Contact:
    """
    Save a new contact to the database.

    Args:
        contact (SendingContact): The contact data to save.
        db (Session): The database session.
        lang (str): The language code to associate with the contact.

    Returns:
        Contact: The saved contact object.
    """
    # Fetch the language object based on the provided language code
    language = db.query(Language).filter(Language.iso639_1 == lang).first()
    if not language:
        raise ValueError(f"Language '{lang}' not found in the database.")

    try:
        new_contact = Contact(
            name=contact.name,
            email=contact.email,
            message=contact.message,
            creation_date=datetime.now(timezone.utc),  # Use timezone from datetime
            sended=False,  # Default value
            language_id=language.id  # Associate the language
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact
    except ValueError as e:
        raise ValueError(f"Validation error: {e}")

