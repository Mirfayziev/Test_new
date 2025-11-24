"""
Utility functions va decorators
"""

from functools import wraps
from flask import flash, redirect, url_for, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os


def role_required(*roles):
    """Role-based access decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Iltimos, tizimga kiring!', 'warning')
                return redirect(url_for('login'))
            
            if current_user.role not in roles:
                flash('Bu sahifaga ruxsatingiz yo\'q!', 'danger')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def module_required(module_name, permission='view'):
    """Modul ruxsatini tekshirish decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            
            # Admin hammaga ruxsati bor
            if current_user.role == 'admin':
                return f(*args, **kwargs)
            
            # Rahbar ko'p ruxsatlar
            if current_user.role == 'rahbar':
                if permission in ['view', 'create', 'edit']:
                    return f(*args, **kwargs)
            
            # Xodim uchun tekshirish
            from modules.models import UserModule
            perm = UserModule.query.filter_by(
                user_id=current_user.id,
                module_name=module_name,
                is_active=True
            ).first()
            
            if not perm or not getattr(perm, f'can_{permission}', False):
                flash('Bu modulga ruxsatingiz yo\'q!', 'danger')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def has_module_permission(user, module_name, permission='view'):
    """Modulga ruxsatni tekshirish (template uchun)"""
    if user.role == 'admin':
        return True
    
    if user.role == 'rahbar':
        return permission in ['view', 'create', 'edit']
    
    from modules.models import UserModule
    perm = UserModule.query.filter_by(
        user_id=user.id,
        module_name=module_name,
        is_active=True
    ).first()
    
    return perm and getattr(perm, f'can_{permission}', False)


def send_telegram_notification(user, title, message):
    """Telegram notification"""
    if not user.telegram_chat_id or not user.telegram_notifications:
        return False
    
    try:
        from telegram_bot import send_notification
        full_message = f"🔔 {title}\n\n{message}"
        return send_notification(user.telegram_chat_id, full_message)
    except:
        return False


def format_date(date_obj):
    """Format date"""
    return date_obj.strftime('%d.%m.%Y') if date_obj else '-'


def format_money(amount):
    """Format money"""
    return f"{amount:,.0f}".replace(',', ' ') if amount else '0'


# =========================== FILE HANDLING ===========================

ALLOWED_EXTENSIONS = {
    'images': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
    'documents': {'pdf', 'doc', 'docx', 'xls', 'xlsx'},
    'all': {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx', 'xls', 'xlsx'}
}


def allowed_file(filename, file_type='all'):
    """Check if file type is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS.get(file_type, ALLOWED_EXTENSIONS['all'])


def save_file(file, subfolder='', prefix=''):
    """Save file and return path"""
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Create unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = filename.rsplit('.', 1)[1].lower()
        
        if prefix:
            filename = f"{prefix}_{timestamp}.{ext}"
        else:
            filename = f"{timestamp}_{filename}"
        
        # Get upload path
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        
        if subfolder:
            upload_path = os.path.join(upload_folder, subfolder)
        else:
            upload_path = upload_folder
        
        # Create folder if not exists
        os.makedirs(upload_path, exist_ok=True)
        
        # Full filepath
        filepath = os.path.join(upload_path, filename)
        
        # Save file
        file.save(filepath)
        
        # Return relative path
        if subfolder:
            return os.path.join(subfolder, filename)
        return filename
    
    return None


def delete_file(filepath):
    """Delete file"""
    if filepath:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        full_path = os.path.join(upload_folder, filepath)
        
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                return True
            except:
                pass
    
    return False

