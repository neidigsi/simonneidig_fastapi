"""
Application configuration loader

Author: Simon Neidig <mail@simonneidig.de>

Loads environment variables (from .env when present) and exposes configuration
values used across the application (e.g. DB connection string).
Keep this module small and focused on configuration resolution only.
"""

# Import external dependencies
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

# Store variables in global accessible variables
DB_CONNECTION = os.getenv('DB_CONNECTION')