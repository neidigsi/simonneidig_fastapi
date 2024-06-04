# Import external dependencies
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

# Store variables in global accessible variables
DB_CONNECTION = os.getenv('DB_CONNECTION')