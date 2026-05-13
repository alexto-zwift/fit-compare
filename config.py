from dotenv import load_dotenv
import os

# Load environment variables from .env file (for local development)
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID", "")
    STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET", "")
    STRAVA_REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI", "http://localhost:5001/auth/callback")
    STRAVA_API_BASE_URL = "https://www.strava.com/api/v3"
    STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"