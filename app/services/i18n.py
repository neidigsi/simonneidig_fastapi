"""
Author: Simon Neidig <mail@simonneidig.de>

Description:
This module provides a utility function for handling internationalization (i18n).

The `get_language` function extracts the preferred language from the `Accept-Language`
header of an incoming HTTP request. It defaults to English ("en") if no language
is specified in the header.
"""

from fastapi import Request


def get_language(request: Request):
    """
    Extract the preferred language from the `Accept-Language` header.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        str: The preferred language code (e.g., "en", "de").
    """
    lang = request.headers.get("accept-language", "en")
    return lang.split(",")[0].strip().lower()  # e.g., "de-DE,de;q=0.9" -> "de"
