from datetime import datetime

class User:
    def __init__(self, id, username, email, profile_picture, strava_id, access_token):
        self.id = id
        self.username = username
        self.email = email
        self.profile_picture = profile_picture
        self.strava_id = strava_id
        self.access_token = access_token
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return f"<User {self.username}>"

    def update_profile(self, username=None, email=None, profile_picture=None):
        if username:
            self.username = username
        if email:
            self.email = email
        if profile_picture:
            self.profile_picture = profile_picture

    def get_strava_data(self):
        # Placeholder for method to fetch data from Strava API
        pass

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "profile_picture": self.profile_picture,
            "strava_id": self.strava_id,
            "created_at": self.created_at.isoformat()
        }