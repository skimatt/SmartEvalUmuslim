import string
import random
import json
import pandas as pd
import plotly
import plotly.express as px



from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from flask_wtf import FlaskForm 
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

# Import semua Model yang dibutuhkan
from models import PendingUser, User, db, Report, ReportComment, Lecturer, Rating 
from app import bcrypt 
from admin.forms import RejectForm, LecturerForm 

admin = Blueprint('admin', __name__, url_prefix='/admin')

# --- FORM KOMENTAR & MIDDLEWARE ---
class AdminCommentForm(FlaskForm):
    komentar = TextAreaField('Balasan / Komentar', validators=[DataRequired()])
    submit = SubmitField('Kirim Balasan')

def admin_required(f):
    """Decorator untuk membatasi akses ke Admin atau Bagian Terkait"""
    @login_required
    def decorated_function(*args, **kwargs):
        allowed_roles = ['admin', 'akademik', 'perpustakaan', 'tu', 'kebersihan', 'bem']
        if current_user.role not in allowed_roles:
            flash('Anda tidak memiliki izin akses ke halaman ini.', 'danger')
            return redirect(url_for('main.home')) 
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# --- Generator Password Acak ---
def generate_random_password(length=10):
    """Menghasilkan password acak dengan huruf, angka, dan simbol."""
    characters = string.ascii_letters + string.digits + '!@#$%^&*'
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# --- Admin Dashboard ---
@admin.route('/dashboard')
@admin_required
def dashboard():
    """Menampilkan ringkasan dan statistik Admin."""
    pending_count = PendingUser.query.filter_by(status='pending').count()
    active_reports_count = Report.query.filter(Report.status.in_(['Pending', 'Diproses'])).count()
    total_ratings_count = Rating.query.count()
        
    return render_template('admin/dashboard.html', 
                           title='Dashboard Admin', 
                           pending_count=pending_count,
                           active_reports_count=active_reports_count,
                           total_ratings_count=total_ratings_count)

# --- Verifikasi Pendaftar ---
@admin.route('/verification')
@admin_required
def verification_list():
    """Menampilkan daftar mahasiswa yang mengajukan akun."""
    pending_users = PendingUser.query.filter_by(status='pending').order_by(PendingUser.tanggal_pengajuan.asc()).all()
    reject_form = RejectForm()
    return render_template('admin/verification_list.html', 
                           title='Verifikasi Pendaftar', 
                           pending_users=pending_users,
                           reject_form=reject_form)

# --- Aksi Terima Pendaftar ---
@admin.route('/verification/accept/<int:pending_id>', methods=['POST'])
@admin_required
def accept_user(pending_id):
    """Menerima permintaan akun dan membuat user baru."""
    pending = PendingUser.query.get_or_404(pending_id)
    if pending.status != 'pending':
        flash('Permintaan ini sudah diproses.', 'warning')
        return redirect(url_for('admin.verification_list'))

    username_baru = pending.nim 
    password_plain = generate_random_password()
    password_hash = bcrypt.generate_password_hash(password_plain).decode('utf-8')

    new_user = User(
        username=username_baru,
        password_hash=password_hash,
        nim=pending.nim,
        nama_lengkap=pending.nama_lengkap,
        email=pending.email,
        prodi=pending.prodi,
        role='mahasiswa',
        is_active=True
    )
    
    pending.status = 'accepted'
    
    try:
        db.session.add(new_user)
        db.session.commit()
        flash(f'✅ AKUN DIBUAT: Mahasiswa {pending.nama_lengkap} diterima. Akun dikirim ke {pending.email}. Password: {password_plain}', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Gagal membuat akun: {e}")
        flash('❌ Gagal membuat akun: Terjadi kesalahan database.', 'danger')
        
    return redirect(url_for('admin.verification_list'))

# --- Aksi Tolak Pendaftar ---
@admin.route('/verification/reject/<int:pending_id>', methods=['POST'])
@admin_required
def reject_user(pending_id):
    """Menolak permintaan akun dan mencatat alasannya."""
    form = RejectForm()
    pending = PendingUser.query.get_or_404(pending_id)
    
    if form.validate_on_submit():
        pending.status = 'rejected'
        pending.alasan_penolakan = form.alasan.data
        db.session.commit()
        flash(f'❌ DITOLAK: Permintaan akun {pending.nim} ditolak. Notifikasi dikirim.', 'info')
        return redirect(url_for('admin.verification_list'))
    
    flash('Gagal menolak. Pastikan alasan penolakan sudah terisi dengan benar.', 'danger')
    return redirect(url_for('admin.verification_list'))


# =========================================================================
# --- KELOLA LAPORAN AKTIF ---
# =========================================================================

@admin.route('/reports')
@admin_required
def manage_reports():
    """Menampilkan daftar semua laporan yang bisa dikelola admin/handler."""
    
    if current_user.role == 'admin':
        reports_query = Report.query.filter(Report.status != 'Arsip')
        title_suffix = "Semua Laporan Aktif"
    else:
        # Handler hanya melihat laporan yang ditugaskan kepada role-nya
        reports_query = Report.query.filter(
            Report.assigned_to_role == current_user.role,
            Report.status.in_(['Pending', 'Diproses'])
        )
        title_suffix = f"Laporan Tugas ({current_user.role.capitalize()})"
        
    status_filter = request.args.get('status')
    if status_filter and status_filter in ['Pending', 'Diproses', 'Selesai']:
        reports_query = reports_query.filter_by(status=status_filter)
        
    reports = reports_query.order_by(Report.created_at.desc()).all()
        
    return render_template('admin/manage_reports.html', 
                           title=f'Kelola Laporan | {title_suffix}', 
                           reports=reports)

@admin.route('/report/<int:report_id>', methods=['GET', 'POST'])
@admin_required
def report_detail(report_id):
    """Menampilkan detail laporan, riwayat komentar, dan form update status/komentar."""
    report = Report.query.get_or_404(report_id)
    comment_form = AdminCommentForm()
    
    # Logika Cek Izin Akses (Penting untuk Role Handler)
    if current_user.role != 'admin' and report.assigned_to_role != current_user.role:
        flash('Anda tidak ditugaskan untuk menangani laporan ini.', 'danger')
        return redirect(url_for('admin.manage_reports'))
    
    if request.method == 'POST':
        # 1. Update Status Laporan (Tombol di luar form)
        new_status = request.form.get('status')
        if new_status and new_status in ['Pending', 'Diproses', 'Selesai', 'Arsip']:
            report.status = new_status
            db.session.commit()
            flash(f'Status laporan berhasil diubah menjadi: {new_status}.', 'success')
            current_app.logger.info(f"STATUS UPDATE: Report {report_id} status changed to {new_status}.")
            return redirect(url_for('admin.report_detail', report_id=report_id))
            
    comments = ReportComment.query.filter_by(report_id=report_id).order_by(ReportComment.created_at.asc()).all()
        
    return render_template('admin/report_detail.html', 
                           title=f'Detail Laporan #{report_id}', 
                           report=report,
                           comment_form=comment_form,
                           comments=comments)

@admin.route('/report/<int:report_id>/comment', methods=['POST'])
@admin_required
def add_comment(report_id):
    """Menambahkan komentar/balasan Admin/Handler pada laporan."""
    report = Report.query.get_or_404(report_id)
    comment_form = AdminCommentForm()
    
    if current_user.role != 'admin' and report.assigned_to_role != current_user.role:
        flash('Anda tidak berhak membalas laporan ini.', 'danger')
        return redirect(url_for('admin.manage_reports'))
    
    if comment_form.validate_on_submit():
        new_comment = ReportComment(
            report_id=report_id,
            user_id=current_user.id,
            komentar=comment_form.komentar.data
        )
        
        if report.status == 'Pending':
            report.status = 'Diproses'
            
        db.session.add(new_comment)
        db.session.commit()
        
        flash('Balasan/Komentar berhasil dikirim!', 'success')
        current_app.logger.info(f"REPORT COMMENT: User {current_user.username} commented on report {report_id}.")
        
    else:
        for field, errors in comment_form.errors.items():
            for error in errors:
                flash(f"Error di Balasan: {error}", 'danger')

    return redirect(url_for('admin.report_detail', report_id=report.id))

# =========================================================================
# --- KELOLA DOSEN (LECTURERS) ---
# =========================================================================

@admin.route('/lecturers')
@admin_required
def manage_lecturers():
    """Menampilkan daftar semua dosen."""
    
    lecturers = Lecturer.query.order_by(Lecturer.nama.asc()).all()
    
    return render_template('admin/manage_lecturers.html',
                           title='Kelola Dosen',
                           lecturers=lecturers)

@admin.route('/lecturer/add', methods=['GET', 'POST'])
@admin.route('/lecturer/edit/<int:lecturer_id>', methods=['GET', 'POST'])
@admin_required
def add_edit_lecturer(lecturer_id=None):
    """Menambah atau mengedit data dosen."""
    
    lecturer = None
    if lecturer_id:
        lecturer = Lecturer.query.get_or_404(lecturer_id)
        # Inisialisasi form dengan obj=lecturer agar data terisi otomatis
        form = LecturerForm(obj=lecturer)
        # Menambahkan ID ke form untuk validasi NIDN unik yang benar
        form.lecturer_id.data = lecturer.id 
        title = 'Edit Dosen'
    else:
        form = LecturerForm()
        title = 'Tambah Dosen Baru'

    if form.validate_on_submit():
        if lecturer:
            # Mode Edit
            lecturer.nama = form.nama.data
            lecturer.nidn = form.nidn.data
            lecturer.fakultas = form.fakultas.data
            flash('Data dosen berhasil diperbarui.', 'success')
        else:
            # Mode Tambah Baru
            new_lecturer = Lecturer(
                nama=form.nama.data,
                nidn=form.nidn.data,
                fakultas=form.fakultas.data
            )
            db.session.add(new_lecturer)
            flash('Dosen baru berhasil ditambahkan.', 'success')
        
        db.session.commit()
        return redirect(url_for('admin.manage_lecturers'))
    
    # Jika mode Edit dan metode GET, data sudah terisi via obj=lecturer
        
    return render_template('admin/add_edit_lecturer.html',
                           title=title,
                           form=form,
                           lecturer=lecturer)

@admin.route('/lecturer/delete/<int:lecturer_id>', methods=['POST'])
@admin_required
def delete_lecturer(lecturer_id):
    """Menghapus data dosen."""
    
    lecturer = Lecturer.query.get_or_404(lecturer_id)
    
    ratings_count = Rating.query.filter_by(lecturer_id=lecturer_id).count()
    if ratings_count > 0:
        flash(f'Tidak dapat menghapus dosen {lecturer.nama} karena sudah memiliki {ratings_count} penilaian terkait.', 'danger')
        return redirect(url_for('admin.manage_lecturers'))
        
    db.session.delete(lecturer)
    db.session.commit()
    
    flash(f'Dosen {lecturer.nama} berhasil dihapus.', 'success')
    return redirect(url_for('admin.manage_lecturers'))

# =========================================================================
# --- DASHBOARD STATISTIK ---
# =========================================================================

@admin.route('/statistics')
@admin_required
def statistics_dashboard():
    """Menampilkan dashboard statistik dan visualisasi data."""
    
    # --- PENTING: Pastikan Plotly & Pandas terinstal! ---
    
    # 1. AMBIL SEMUA DATA UNTUK ANALISIS
    all_reports = Report.query.all()
    all_ratings = Rating.query.all()
    all_lecturers = Lecturer.query.all()

    # Inisialisasi list untuk data frame
    report_data = []
    rating_data = []
    
    # Siapkan data Laporan
    for r in all_reports:
        report_data.append({
            'kategori': r.kategori,
            'status': r.status,
            'assigned_to': r.assigned_to_role,
            'bulan': r.created_at.strftime('%Y-%m')
        })
        
    # Siapkan data Rating
    for r in all_ratings:
        lecturer = next((l for l in all_lecturers if l.id == r.lecturer_id), None)
        if lecturer:
            rating_data.append({
                'lecturer_id': r.lecturer_id,
                'lecturer_name': lecturer.nama,
                'fakultas': lecturer.fakultas,
                'mengajar': float(r.rating_mengajar),
                'tugas': float(r.rating_tugas),
                'materi': float(r.rating_materi),
                'avg_rating': (float(r.rating_mengajar) + float(r.rating_tugas) + float(r.rating_materi)) / 3
            })

    # Konversi ke Pandas DataFrame (Handle empty data)
    df_reports = pd.DataFrame(report_data)
    df_ratings = pd.DataFrame(rating_data)

    graph_trend = None
    graph_category = None
    graph_ranking = None
    top_lecturers = []

    # --- VISUALISASI 1: Trend Laporan per Bulan ---
    if not df_reports.empty:
        trend_data = df_reports.groupby('bulan').size().reset_index(name='jumlah')
        fig_trend = px.line(trend_data, x='bulan', y='jumlah', title='Trend Laporan Masuk per Bulan')
        graph_trend = json.dumps(fig_trend, cls=plotly.utils.PlotlyJSONEncoder)

    # --- VISUALISASI 2: Distribusi Laporan per Kategori ---
    if not df_reports.empty:
        category_data = df_reports['kategori'].value_counts().reset_index()
        category_data.columns = ['kategori', 'jumlah']
        fig_category = px.pie(category_data, names='kategori', values='jumlah', title='Distribusi Laporan berdasarkan Kategori')
        graph_category = json.dumps(fig_category, cls=plotly.utils.PlotlyJSONEncoder)

    # --- VISUALISASI 3: Ranking Dosen Terbaik ---
    if not df_ratings.empty:
        # Hitung Rata-rata Rating per Dosen
        avg_ratings = df_ratings.groupby(['lecturer_id', 'lecturer_name', 'fakultas'])[['avg_rating']].mean().reset_index()
        avg_ratings = avg_ratings.sort_values(by='avg_rating', ascending=False).head(10)
        
        # Buat grafik bar Top 10
        fig_ranking = px.bar(avg_ratings, 
                             x='lecturer_name', 
                             y='avg_rating', 
                             color='fakultas',
                             title='Top 10 Dosen Berdasarkan Rata-rata Rating',
                             labels={'lecturer_name': 'Nama Dosen', 'avg_rating': 'Rata-rata Rating'})
        graph_ranking = json.dumps(fig_ranking, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Ambil data ranking untuk tabel
        top_lecturers = avg_ratings.to_dict('records')
        
    return render_template('admin/statistics_dashboard.html',
                           title='Dashboard Statistik & Evaluasi',
                           graph_trend=graph_trend,
                           graph_category=graph_category,
                           graph_ranking=graph_ranking,
                           top_lecturers=top_lecturers)

