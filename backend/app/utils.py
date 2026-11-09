from functools import wraps
from flask import current_app, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.utilisateur import Utilisateur


def auth_required(f):
    """Remplace @jwt_required(). Ne fait rien si AUTH_ENABLED = False."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_app.config.get("AUTH_ENABLED", True):
            return f(*args, **kwargs)  # auth en pause
        verify_jwt_in_request()
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    """Remplace tes vérifications de rôle admin."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_app.config.get("AUTH_ENABLED", True):
            return f(*args, **kwargs)  # auth en pause
        verify_jwt_in_request()
        user = Utilisateur.query.get(get_jwt_identity())
        if not user or user.role != "admin":
            return jsonify({"message": "Accès refusé"}), 403
        return f(*args, **kwargs)
    return wrapper