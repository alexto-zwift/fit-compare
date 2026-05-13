import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Handler for Vercel
def handler(request):
    """Vercel serverless function handler"""
    return app(request.environ, request.start_response)
