from flask import current_app, session
import requests

class StravaClient:
    def __init__(self):
        self.base_url = "https://www.strava.com/api/v3"
        self.access_token = None

    def set_access_token(self, token):
        self.access_token = token

    def get_athlete(self):
        if not self.access_token:
            raise ValueError("Access token is not set.")
        
        url = f"{self.base_url}/athlete"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            current_app.logger.error(f"Error fetching athlete data: {response.status_code} - {response.text}")
            response.raise_for_status()

    def get_activities(self, page=1, per_page=30):
        if not self.access_token:
            raise ValueError("Access token is not set.")
        
        url = f"{self.base_url}/athlete/activities"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"page": page, "per_page": per_page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            current_app.logger.error(f"Error fetching activities: {response.status_code} - {response.text}")
            response.raise_for_status()


def get_user_profile():
    """Get the user profile from Strava using the access token in session."""
    access_token = session.get('access_token')
    if not access_token:
        return None
    
    client = StravaClient()
    client.set_access_token(access_token)
    try:
        return client.get_athlete()
    except Exception as e:
        current_app.logger.error(f"Error getting user profile: {e}")
        return None


def get_user_activities():
    """Get the user activities from Strava using the access token in session."""
    access_token = session.get('access_token')
    if not access_token:
        return None
    
    client = StravaClient()
    client.set_access_token(access_token)
    try:
        return client.get_activities()
    except Exception as e:
        current_app.logger.error(f"Error getting user activities: {e}")
        return None