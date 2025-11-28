import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Centralized configuration for the application.
    This keeps paths and keys in one place.
    """
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Base Directory (Root of the project)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # Data Directories
    DATA_DIR = BASE_DIR / "data"
    INPUT_DIR = DATA_DIR / "input"
    OUTPUT_DIR = DATA_DIR / "output"
    
    # Template Directory
    TEMPLATES_DIR = BASE_DIR / "src" / "templates"

    @classmethod
    def validate(cls):
        """Checks if essential configuration is present."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("❌ GOOGLE_API_KEY is missing. Please add it to your .env file.")
        
        # Ensure directories exist
        cls.INPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Run validation on import to fail fast if something is wrong
Config.validate()