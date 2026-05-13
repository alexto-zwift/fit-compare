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

    def get_activity(self, activity_id):
        if not self.access_token:
            raise ValueError("Access token is not set.")

        url = f"{self.base_url}/activities/{activity_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()

        current_app.logger.error(
            f"Error fetching activity {activity_id}: {response.status_code} - {response.text}"
        )
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
        status_code = getattr(getattr(e, "response", None), "status_code", None)
        if status_code == 401 and _refresh_access_token():
            try:
                client.set_access_token(session.get('access_token'))
                return client.get_athlete()
            except Exception as retry_error:
                current_app.logger.error(f"Error getting user profile after token refresh: {retry_error}")
                return None
        current_app.logger.error(f"Error getting user profile: {e}")
        return None


def get_user_activities(user_profile=None):
    """Get the user activities from Strava using the access token in session."""
    access_token = session.get('access_token')
    if not access_token:
        return None
    
    client = StravaClient()
    client.set_access_token(access_token)
    try:
        activities = client.get_activities()
        return _enrich_group_people(activities, user_profile, client)
    except Exception as e:
        status_code = getattr(getattr(e, "response", None), "status_code", None)
        if status_code == 401 and _refresh_access_token():
            try:
                client.set_access_token(session.get('access_token'))
                activities = client.get_activities()
                return _enrich_group_people(activities, user_profile, client)
            except Exception as retry_error:
                current_app.logger.error(f"Error getting user activities after token refresh: {retry_error}")
                return None
        current_app.logger.error(f"Error getting user activities: {e}")
        return None


def _enrich_group_people(activities, user_profile, client):
    if not activities:
        return activities

    owner_id = user_profile.get('id') if user_profile else None
    owner_name = "You"
    if user_profile:
        first = user_profile.get('firstname', '')
        last = user_profile.get('lastname', '')
        owner_name = f"{first} {last}".strip() or user_profile.get('username') or "You"

    enriched = []
    for activity in activities:
        people = []

        if owner_id:
            people.append({
                'id': owner_id,
                'name': owner_name,
                'url': f"https://www.strava.com/athletes/{owner_id}"
            })

        # Strava summary activities do not always expose group member names.
        # When athlete_count > 1, try detailed activity payload for extra people fields.
        if activity.get('athlete_count', 1) > 1:
            try:
                detailed = client.get_activity(activity.get('id'))
                _merge_people(people, detailed.get('group_members'))
                _merge_people(people, detailed.get('athletes'))
            except Exception as detail_error:
                current_app.logger.warning(
                    f"Could not enrich group members for activity {activity.get('id')}: {detail_error}"
                )

        activity['group_people'] = people
        enriched.append(activity)

    return enriched


def _merge_people(target, source):
    if not source or not isinstance(source, list):
        return

    existing = {(p.get('id'), p.get('name')) for p in target}
    for person in source:
        if not isinstance(person, dict):
            continue

        person_id = person.get('id')
        name = _person_name(person)
        if not name:
            continue

        key = (person_id, name)
        if key in existing:
            continue

        target.append({
            'id': person_id,
            'name': name,
            'url': f"https://www.strava.com/athletes/{person_id}" if person_id else None
        })
        existing.add(key)


def _person_name(person):
    first = person.get('firstname')
    last = person.get('lastname')
    full = f"{first or ''} {last or ''}".strip()
    return full or person.get('username') or person.get('name')


def _refresh_access_token():
    """Refresh Strava access token using refresh token from session."""
    refresh_token = session.get('refresh_token')
    if not refresh_token:
        return False

    token_response = requests.post(current_app.config['STRAVA_TOKEN_URL'], data={
        'client_id': current_app.config['STRAVA_CLIENT_ID'],
        'client_secret': current_app.config['STRAVA_CLIENT_SECRET'],
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    })

    if token_response.status_code != 200:
        current_app.logger.error(
            f"Failed to refresh Strava token: {token_response.status_code} - {token_response.text}"
        )
        return False

    token_data = token_response.json()
    new_access_token = token_data.get('access_token')
    if not new_access_token:
        current_app.logger.error(f"Refresh response missing access token: {token_data}")
        return False

    session['access_token'] = new_access_token
    if token_data.get('refresh_token'):
        session['refresh_token'] = token_data.get('refresh_token')
    if token_data.get('expires_at'):
        session['expires_at'] = token_data.get('expires_at')

    return True