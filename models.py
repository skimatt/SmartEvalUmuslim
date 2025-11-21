from app import db, login_manager, bcrypt # <-- Tambahkan 'bcrypt' dan 'login_manager'
from datetime import datetime
from sqlalchemy import Enum
from flask_login import UserMixin # <-- Kelas dasar untuk Flask-Login

# Fungsi untuk memuat user dari sesi (wajib untuk Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    """
    Fungsi ini dipanggil oleh Flask-Login untuk memuat objek User
    dari ID pengguna yang disimpan dalam sesi.
    """
    return User.query.get(int(user_id))

# --- MODEL UTAMA ---

# Menggunakan UserMixin agar Flask-Login dapat bekerja
class User(db.Model, UserMixin): # <-- Mewarisi UserMixin
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
    reports = db.relationship('Report', backref='mahasiswa', lazy=True)
    ratings = db.relationship('Rating', backref='mahasiswa', lazy=True)
    comments = db.relationship('ReportComment', backref='user', lazy=True)

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

# --- MODEL LAINNYA (TIDAK BERUBAH) ---

class Lecturer(db.Model):
    """Tabel Master Dosen"""
    __tablename__ = 'lecturers'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=False)
    nidn = db.Column(db.String(20), unique=True)
    fakultas = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    ratings = db.relationship('Rating', backref='lecturer', lazy=True)

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

class Report(db.Model):
    """Tabel Laporan Kampus"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    judul = db.Column(db.String(255), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    kategori = db.Column(Enum('Fasilitas', 'Layanan TU', 'Perpustakaan', 'Akademik', 'Lainnya', name='report_kategori_enum'), nullable=False)
    status = db.Column(Enum('Pending', 'Diproses', 'Selesai', 'Arsip', name='report_status_enum'), default='Pending')
    assigned_to_role = db.Column(Enum('akademik', 'perpustakaan', 'tu', 'kebersihan', 'bem', name='assigned_role_enum'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = db.relationship('ReportComment', backref='report', lazy=True)

class ReportComment(db.Model):
    """Tabel Komentar Laporan"""
    __tablename__ = 'report_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    komentar = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Rating(db.Model):
    """Tabel Penilaian Dosen"""
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'), nullable=False)
    rating_mengajar = db.Column(db.DECIMAL(2, 1), nullable=False) 
    rating_tugas = db.Column(db.DECIMAL(2, 1), nullable=False)
    rating_materi = db.Column(db.DECIMAL(2, 1), nullable=False)
    komentar = db.Column(db.Text)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('mahasiswa_id', 'lecturer_id', name='uc_mahasiswa_dosen'),)