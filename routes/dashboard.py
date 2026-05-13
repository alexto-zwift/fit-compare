from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.strava_client import get_user_activities, get_user_profile

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    # Check if user is authenticated
    if 'access_token' not in session:
        flash('Please log in with Strava first.', 'warning')
        return redirect(url_for('auth.login'))
    
    user_profile = get_user_profile()
    user_activities = get_user_activities()
    
    if user_profile is None or user_activities is None:
        flash('Error retrieving data from Strava. Please try again later.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('dashboard.html', profile=user_profile, activities=user_activities)