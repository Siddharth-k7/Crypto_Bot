import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    COINGECKO_API_KEY = os.environ.get('COINGECKO_API_KEY')
    # Add other settings as needed

# Usage in app.py:
# from config import Config
# app.config.from_object(Config)
