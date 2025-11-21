from app import db, bcrypt
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Enum

# Menggunakan UserMixin agar Flask-Login dapat bekerja
class User(db.Model, UserMixin): 
    """Tabel Pengguna (Admin, Mahasiswa, Handler)"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nim = db.Column(db.String(15), unique=True)
    nama_lengkap = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    prodi = db.Column(db.String(100))
    role = db.Column(Enum('admin', 'mahasiswa', 'akademik', 'perpustakaan', 'tu', 'kebersihan', 'bem', name='user_role_enum'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Hubungan (Relationships)
    # Relasi ke Report (mahasiswa.reports) diatur di model Report
    # Relasi ke Rating (mahasiswa.ratings) diatur di model Rating
    # Relasi ke Comment (user.comments) diatur di model ReportComment

    # 1. Properti untuk mengatur password (otomatis di-hash)
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """Menerima password plain-text dan menyimpannya sebagai hash."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # 2. Metode untuk memverifikasi password
    def verify_password(self, password):
        """Memverifikasi password plain-text terhadap hash yang tersimpan."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class PendingUser(db.Model):
    """Tabel Pengguna Tertunda (Verifikasi Akun)"""
    __tablename__ = 'pending_users'
    
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(15), unique=True, nullable=False)
    nama_lengkap = db.Column(db.String(150), nullable=False)
    prodi = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    hp = db.Column(db.String(20))
    bukti_url = db.Column(db.String(255), nullable=False) 
    status = db.Column(Enum('pending', 'accepted', 'rejected', name='pending_status_enum'), default='pending')
    alasan_penolakan = db.Column(db.Text)
    tanggal_pengajuan = db.Column(db.DateTime, default=datetime.utcnow)