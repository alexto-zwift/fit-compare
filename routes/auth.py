from flask import Blueprint, redirect, url_for, session, request
import requests
from flask import current_app
from urllib.parse import urlencode

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    # Build the Strava OAuth URL dynamically
    client_id = current_app.config.get('STRAVA_CLIENT_ID')
    redirect_uri = current_app.config.get('STRAVA_REDIRECT_URI')
    
    if not client_id:
        return "Error: STRAVA_CLIENT_ID not configured. Please check your .env file.", 400
    
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'approval_prompt': 'force',
        'scope': 'profile:read_all,activity:read_all'
    }
    
    strava_auth_url = f"https://www.strava.com/oauth/authorize?{urlencode(params)}"
    return redirect(strava_auth_url)

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    token_response = requests.post(current_app.config['STRAVA_TOKEN_URL'], data={
        'client_id': current_app.config['STRAVA_CLIENT_ID'],
        'client_secret': current_app.config['STRAVA_CLIENT_SECRET'],
        'code': code,
        'grant_type': 'authorization_code'
    })
    token_data = token_response.json()
    session.permanent = True
    session['access_token'] = token_data.get('access_token')
    session['refresh_token'] = token_data.get('refresh_token')
    return redirect(url_for('dashboard.dashboard'))