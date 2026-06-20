import os
from dotenv import load_dotenv

# Locate the parent directory of this file and load the .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Flask application configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-flight-system-secret-key-999')
    
    # Retrieve DATABASE_URL or use a fresh temporary SQLite DB on Vercel to bypass IPv6 connection limits
    if os.getenv('VERCEL') == '1':
        db_url = 'sqlite:////tmp/flights.db'
    else:
        db_url = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "flights.db")}')
        if db_url and db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Gemini API Credentials
    # DO NOT hardcode the API key here or GitHub will block the push!
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
