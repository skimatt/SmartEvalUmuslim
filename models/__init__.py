# Import objek inti (db, bcrypt) langsung dari app untuk menghindari circular import
from app import db, login_manager, bcrypt 
from flask_login import UserMixin 
from datetime import datetime
from sqlalchemy import Enum 

# Panggil fungsi load_user di sini agar Flask-Login bekerja
@login_manager.user_loader
def load_user(user_id):
    """Fungsi ini dipanggil oleh Flask-Login untuk memuat objek User."""
    from .user import User # <-- Import di sini untuk menghindari circular import
    return User.query.get(int(user_id))

# Link semua model agar dikenali oleh SQLAlchemy saat db.create_all() dipanggil
from .user import User, PendingUser
from .report import Report, ReportComment
from .rating import Lecturer, Rating