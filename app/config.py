
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def validate():
        if not Settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

# Initialize settings
settings = Settings()
settings.validate()