from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.strava_client import get_user_activities, get_user_profile

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    # Check if user is authenticated
    if not session.get('access_token'):
        flash('Please log in with Strava first.', 'warning')
        return redirect(url_for('auth.login'))
    
    user_profile = get_user_profile()
    user_activities = get_user_activities(user_profile=user_profile)
    
    if user_profile is None or user_activities is None:
        flash('Logged in, but unable to load Strava data right now. Please try again shortly.', 'warning')
        return render_template('dashboard.html', profile={}, activities=[])

    return render_template('dashboard.html', profile=user_profile, activities=user_activities)