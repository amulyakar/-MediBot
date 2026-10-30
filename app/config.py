
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Read Groq configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

# Check whether the API key exists
def check_groq_configuration():
    if not GROQ_API_KEY:
        return False

    return True
