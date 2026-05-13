from flask import Blueprint, redirect, url_for, session, request, flash
import requests
from flask import current_app
from urllib.parse import urlencode

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    # If user is already authenticated in this session, avoid forcing OAuth again.
    if session.get('access_token'):
        return redirect(url_for('dashboard.dashboard'))

    # Build the Strava OAuth URL dynamically.
    # Prefer request host so preview/prod Vercel domains both work without env drift.
    client_id = current_app.config.get('STRAVA_CLIENT_ID')
    configured_redirect_uri = current_app.config.get('STRAVA_REDIRECT_URI')
    request_base = request.url_root.rstrip('/')
    redirect_uri = configured_redirect_uri or f"{request_base}{url_for('auth.callback')}"

    # If running on Vercel, always use current host callback to avoid cross-domain session issues.
    if request.host.endswith('.vercel.app'):
        redirect_uri = f"{request_base}{url_for('auth.callback')}"
    
    if not client_id:
        return "Error: STRAVA_CLIENT_ID not configured. Please check your .env file.", 400
    
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'approval_prompt': 'auto',
        'scope': 'profile:read_all,activity:read_all'
    }

    # Persist redirect_uri so token exchange uses the same value Strava received.
    session['oauth_redirect_uri'] = redirect_uri
    
    strava_auth_url = f"https://www.strava.com/oauth/authorize?{urlencode(params)}"
    return redirect(strava_auth_url)

@auth_bp.route('/callback')
def callback():
    if request.args.get('error'):
        flash('Strava authorization was canceled or failed.', 'warning')
        return redirect(url_for('home'))

    code = request.args.get('code')
    if not code:
        flash('Missing authorization code from Strava.', 'danger')
        return redirect(url_for('home'))

    redirect_uri = (
        session.get('oauth_redirect_uri')
        or current_app.config.get('STRAVA_REDIRECT_URI')
        or f"{request.url_root.rstrip('/')}{url_for('auth.callback')}"
    )

    token_response = requests.post(current_app.config['STRAVA_TOKEN_URL'], data={
        'client_id': current_app.config['STRAVA_CLIENT_ID'],
        'client_secret': current_app.config['STRAVA_CLIENT_SECRET'],
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    })

    if token_response.status_code != 200:
        current_app.logger.error(f"Strava token exchange failed: {token_response.status_code} - {token_response.text}")
        flash('Unable to complete Strava login. Please try again.', 'danger')
        return redirect(url_for('home'))

    token_data = token_response.json()
    access_token = token_data.get('access_token')
    if not access_token:
        current_app.logger.error(f"Strava token response missing access token: {token_data}")
        flash('Strava login did not return an access token.', 'danger')
        return redirect(url_for('home'))

    session.permanent = True
    session['access_token'] = access_token
    session['refresh_token'] = token_data.get('refresh_token')
    session['expires_at'] = token_data.get('expires_at')
    session.pop('oauth_redirect_uri', None)
    return redirect(url_for('dashboard.dashboard'))