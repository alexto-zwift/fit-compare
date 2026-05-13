from flask import session

def store_token(token):
    session['strava_token'] = token

def get_token():
    return session.get('strava_token')

def clear_token():
    session.pop('strava_token', None)