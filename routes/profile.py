from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.strava_client import get_user_profile

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/profile")
def profile():
    # Check if user is authenticated
    if not session.get('access_token'):
        flash('Please log in with Strava first.', 'warning')
        return redirect(url_for('auth.login'))
    
    user_info = get_user_profile()
    if user_info is None:
        flash("Logged in, but unable to fetch profile information right now.", "warning")
        return render_template("profile.html", user={})
    return render_template("profile.html", user=user_info)