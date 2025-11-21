from app import db 
from datetime import datetime
from sqlalchemy import Enum

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
    
    # --- KOLOM YANG HILANG (PERBAIKAN) ---
    bukti_url = db.Column(db.String(255), nullable=True) # Dibuat nullable karena laporan mungkin tidak selalu melampirkan bukti
    # --------------------------------------
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = db.relationship('ReportComment', backref='report', lazy=True)
    mahasiswa = db.relationship('User', backref='reports', lazy=True) 

class ReportComment(db.Model):
    """Tabel Komentar Laporan"""
    __tablename__ = 'report_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    komentar = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='comments', lazy=True)