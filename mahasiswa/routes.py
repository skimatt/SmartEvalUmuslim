import string
import random
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask import current_app

# Import Form yang sudah kita buat
from mahasiswa.forms import ReportForm, RatingForm
# Import Model dari package models
from models import Report, db, User, Lecturer, Rating, ReportComment
from app import proofs # PENTING: Import proofs untuk upload file
from werkzeug.utils import secure_filename

mahasiswa = Blueprint('mahasiswa', __name__, url_prefix='/mahasiswa')

# --- Middleware Kustom untuk Cek Role Mahasiswa ---
def mahasiswa_required(f):
    """Membatasi akses hanya untuk user dengan role 'mahasiswa'."""
    @login_required
    def decorated_function(*args, **kwargs):
        # Memastikan user adalah Mahasiswa 
        if current_user.role != 'mahasiswa':
            flash('Halaman ini hanya untuk Mahasiswa.', 'danger')
            return redirect(url_for('main.home')) 
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# --- Dashboard Mahasiswa ---
@mahasiswa.route('/dashboard')
@mahasiswa_required
def dashboard():
    """Menampilkan dashboard dan ringkasan laporan mahasiswa."""
    # Ambil laporan milik user saat ini
    my_reports = Report.query.filter_by(mahasiswa_id=current_user.id).order_by(Report.created_at.desc()).all()
    
    return render_template('mahasiswa/dashboard.html', 
                           title='Dashboard Mahasiswa', 
                           reports=my_reports)

# --- Membuat Laporan Baru (DENGAN FILE UPLOAD OPSIONAL) ---
@mahasiswa.route('/create_report', methods=['GET', 'POST'])
@mahasiswa_required
def create_report():
    """Halaman untuk mengisi dan mengirim laporan baru."""
    form = ReportForm()
    
    if form.validate_on_submit():
        
        bukti_url = None
        
        # 1. Cek dan Simpan File Bukti (Opsional)
        if form.bukti_laporan.data:
            try:
                # Membuat nama file unik (NIM_timestamp_namafile)
                filename = proofs.save(form.bukti_laporan.data, name=current_user.nim + '_report_')
                bukti_url = proofs.url(filename) # Path relatif ke file yang disimpan
                current_app.logger.info(f"Report File Upload Success: {bukti_url}")
            except Exception as e:
                current_app.logger.error(f"File Upload Error: {e}")
                flash('❌ Gagal mengunggah file bukti. Laporkan masalah tanpa bukti, atau coba lagi.', 'danger')
                return redirect(url_for('mahasiswa.create_report'))
                
        
        # 2. Menentukan assigned_to_role berdasarkan kategori
        assigned_role = 'admin'
        if form.kategori.data == 'Fasilitas':
            assigned_role = 'kebersihan'
        elif form.kategori.data in ['Layanan TU', 'Akademik']:
            assigned_role = 'akademik'
        elif form.kategori.data == 'Perpustakaan':
            assigned_role = 'perpustakaan'
        
        # 3. Buat dan simpan laporan
        new_report = Report(
            mahasiswa_id=current_user.id,
            judul=form.judul.data,
            deskripsi=form.deskripsi.data,
            kategori=form.kategori.data,
            assigned_to_role=assigned_role,
            status='Pending',
            bukti_url=bukti_url
        )
        
        db.session.add(new_report)
        db.session.commit()
        
        flash('Laporan Anda berhasil dikirim dan akan segera diproses oleh Bagian Terkait.', 'success')
        return redirect(url_for('mahasiswa.dashboard'))
        
    return render_template('mahasiswa/create_report.html', 
                           title='Buat Laporan Baru', 
                           form=form)

# --- Lihat Detail Laporan (BARU) ---
@mahasiswa.route('/report/<int:report_id>')
@mahasiswa_required
def report_detail(report_id):
    """Menampilkan detail laporan dan riwayat komentar."""
    
    report = Report.query.get_or_404(report_id)
    
    # PENTING: Pastikan hanya pemilik laporan yang bisa melihat detail
    if report.mahasiswa_id != current_user.id:
        flash('Anda tidak memiliki izin untuk melihat laporan ini.', 'danger')
        return redirect(url_for('mahasiswa.dashboard'))
        
    # Ambil komentar terkait
    comments = ReportComment.query.filter_by(report_id=report_id).order_by(ReportComment.created_at.asc()).all()
    
    return render_template('mahasiswa/report_detail.html',
                           title=f'Detail Laporan #{report_id}',
                           report=report,
                           comments=comments)


# --- Daftar Dosen untuk Dinilai ---
@mahasiswa.route('/rate_lecturers')
@mahasiswa_required
def rate_lecturers():
    """Menampilkan daftar dosen yang perlu dinilai."""
    
    lecturers = Lecturer.query.order_by(Lecturer.nama.asc()).all()
    
    rated_lecturer_ids = [r.lecturer_id for r in current_user.ratings]
    
    return render_template('mahasiswa/rate_lecturers.html',
                           title='Penilaian Dosen',
                           lecturers=lecturers,
                           rated_lecturer_ids=rated_lecturer_ids)

# --- Submit Rating ---
@mahasiswa.route('/rate_lecturers/<int:lecturer_id>', methods=['GET', 'POST'])
@mahasiswa_required
def submit_rating(lecturer_id):
    """Form untuk memberikan rating pada dosen tertentu."""
    lecturer = Lecturer.query.get_or_404(lecturer_id)
    
    existing_rating = Rating.query.filter_by(mahasiswa_id=current_user.id, lecturer_id=lecturer_id).first()
    if existing_rating:
        flash('Anda sudah memberikan penilaian untuk dosen ini.', 'info')
        return redirect(url_for('mahasiswa.rate_lecturers'))
        
    form = RatingForm()
    
    if form.validate_on_submit():
        
        if Rating.query.filter_by(mahasiswa_id=current_user.id, lecturer_id=lecturer_id).first():
            flash('Penilaian ganda tidak diperbolehkan.', 'danger')
            return redirect(url_for('mahasiswa.rate_lecturers'))
            
        new_rating = Rating(
            mahasiswa_id=current_user.id,
            lecturer_id=lecturer_id,
            rating_mengajar=float(form.rating_mengajar.data),
            rating_tugas=float(form.rating_tugas.data),
            rating_materi=float(form.rating_materi.data),
            komentar=form.komentar.data
        )
        
        db.session.add(new_rating)
        db.session.commit()
        flash(f'Terima kasih! Penilaian untuk Dosen {lecturer.nama} berhasil disimpan.', 'success')
        return redirect(url_for('mahasiswa.rate_lecturers'))
        
    return render_template('mahasiswa/submit_rating.html',
                           title=f'Nilai Dosen: {lecturer.nama}',
                           form=form,
                           lecturer=lecturer)