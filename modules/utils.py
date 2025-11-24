import os
from functools import wraps
from flask import flash, redirect, url_for, current_app
from flask_login import current_user

def role_required(*roles):
    """Decorator: allow only users with given roles."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("login"))
            if roles and current_user.role not in roles:
                flash("Ruxsat yo'q!", "danger")
                return redirect(url_for("dashboard"))
            return f(*args, **kwargs)
        return wrapped
    return decorator

def module_required(module_name):
    """Decorator: simple on/off by role. Extend later if needed."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # If you later add per-module permissions, check here.
            return f(*args, **kwargs)
        return wrapped
    return decorator

UPLOAD_DIR = os.getenv("UPLOAD_FOLDER", "uploads")

def save_file(file_storage):
    """Save uploaded file and return relative path."""
    if not file_storage or file_storage.filename == "":
        return None
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = file_storage.filename
    path = os.path.join(UPLOAD_DIR, filename)
    file_storage.save(path)
    return path

def delete_file(path):
    """Delete file if exists."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
            return True
    except Exception:
        pass
    return False
