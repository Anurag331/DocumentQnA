import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Document QA API"
    VERSION: str = "1.0.0"
    
    # API Keys
    OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
    PINECONE_API_KEY: str | None = os.getenv("PINECONE_API_KEY")
    
    # Validation check to ensure keys exist when the app starts
    def validate_keys(self):
        if not self.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is missing from .env file.")
        if not self.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is missing from .env file.")

settings = Settings()