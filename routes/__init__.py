from flask import Blueprint

routes = Blueprint('routes', __name__)

from .auth import auth_bp
from .dashboard import dashboard_bp
from .profile import profile_bp

__all__ = ['auth_bp', 'dashboard_bp', 'profile_bp']