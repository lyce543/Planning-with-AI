import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Credentials:
    api_key = os.getenv("OPENROUTER_API_KEY")
    database_url = os.getenv("DATABASE_URL")
