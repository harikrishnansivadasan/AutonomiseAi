import re
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.

    Args:
        text (str): The extracted text to be cleaned.
    Returns:
        str: Cleaned and normalized text.
    """
    text = text.replace("\\n", "\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


class GroqConfig:

    def __init__(self, api_key=None, model="meta-llama/llama-4-scout-17b-16e-instruct"):
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)
        self.model = model
