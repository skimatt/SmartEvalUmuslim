from app import db 
from datetime import datetime
from sqlalchemy import UniqueConstraint

class Lecturer(db.Model):
    """Tabel Master Dosen"""
    __tablename__ = 'lecturers'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=False)
    nidn = db.Column(db.String(20), unique=True)
    fakultas = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    ratings = db.relationship('Rating', backref='lecturer', lazy=True)

class Rating(db.Model):
    """Tabel Penilaian Dosen"""
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    # Kunci asing ke tabel 'users'
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'), nullable=False)
    rating_mengajar = db.Column(db.DECIMAL(2, 1), nullable=False) 
    rating_tugas = db.Column(db.DECIMAL(2, 1), nullable=False)
    rating_materi = db.Column(db.DECIMAL(2, 1), nullable=False)
    komentar = db.Column(db.Text)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    
    # --- PERBAIKAN: Definisi relasi di sisi Rating ---
    # Ini menciptakan atribut 'ratings' pada objek User (current_user.ratings)
    mahasiswa = db.relationship('User', backref='ratings', lazy=True) 
    # ------------------------------------------------
    
    __table_args__ = (UniqueConstraint('mahasiswa_id', 'lecturer_id', name='uc_mahasiswa_dosen'),)