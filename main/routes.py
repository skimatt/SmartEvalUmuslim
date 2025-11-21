import string
import random
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from main.forms import LoginForm, RequestAccountForm

# Import Model dari package models dan UploadSet proofs dari app
from models import User, PendingUser, db, Report, Rating 
from app import bcrypt, proofs # <-- Tambahkan proofs
from werkzeug.utils import secure_filename # Untuk mengamankan nama file

main = Blueprint('main', __name__)

# --- Halaman Utama ---
@main.route('/')
@main.route('/home')
def home():
    """Halaman Landing Page dengan statistik ringan."""
    
    try:
        total_laporan = Report.query.count()
        total_evaluasi = Rating.query.count()
        
        latest_reports = Report.query.filter(Report.status.in_(['Diproses', 'Selesai'])).order_by(Report.updated_at.desc()).limit(3).all()

        return render_template('home.html', 
                               title='Selamat Datang',
                               total_laporan=total_laporan,
                               total_evaluasi=total_evaluasi,
                               latest_reports=latest_reports)
    except Exception as e:
        current_app.logger.error(f"Database Error on Home: {e}")
        return render_template('home.html', 
                               title='Selamat Datang',
                               total_laporan=0,
                               total_evaluasi=0,
                               latest_reports=[])

# --- Login User ---
@main.route('/login', methods=['GET', 'POST'])
def login():
    """Menangani proses login pengguna."""
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard')) 
        return redirect(url_for('mahasiswa.dashboard')) 

    form = LoginForm()
    if form.validate_on_submit():
        username_or_email = form.username.data
        
        user = User.query.filter_by(username=username_or_email).first()
        if not user:
             user = User.query.filter_by(email=username_or_email).first()

        
        if user:
            current_app.logger.info(f"LOGIN ATTEMPT: User '{username_or_email}' found. Checking password hash...")
            
            if user.verify_password(form.password.data):
                login_user(user)
                current_app.logger.info(f"LOGIN SUCCESS: User '{user.username}' logged in.")
                
                next_page = request.args.get('next')
                flash(f'Selamat datang, {user.nama_lengkap}!', 'success')
                
                if user.role == 'admin':
                    return redirect(next_page or url_for('admin.dashboard'))
                return redirect(next_page or url_for('mahasiswa.dashboard'))
            else:
                current_app.logger.warning(f"LOGIN FAILED: Invalid password for user '{username_or_email}'.")
                flash('Login Gagal. Cek kembali Username/NIM dan Password Anda.', 'danger')
        else:
            current_app.logger.warning(f"LOGIN FAILED: User '{username_or_email}' not found in database.")
            flash('Login Gagal. Cek kembali Username/NIM dan Password Anda.', 'danger')
            
    return render_template('login.html', title='Login SmartEval', form=form)

# --- Logout User ---
@main.route('/logout')
def logout():
    """Menangani proses logout pengguna."""
    logout_user()
    flash('Anda telah logout.', 'success')
    return redirect(url_for('main.home'))

# --- Pengajuan Akun Mahasiswa (DENGAN FILE UPLOAD) ---
@main.route('/request_account', methods=['GET', 'POST'])
def request_account():
    """Halaman pengajuan akun baru oleh mahasiswa."""
    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestAccountForm()
    if form.validate_on_submit():
        
        # 1. Simpan File Bukti (KTM/KRS) ke disk
        try:
            # Membuat nama file unik berdasarkan NIM + nama file asli
            filename = proofs.save(form.bukti_upload.data, name=form.nim.data + '.')
            # URL yang disimpan di DB adalah path relatif dari folder uploads
            bukti_url = proofs.url(filename) 
        except Exception as e:
            current_app.logger.error(f"File Upload Error: {e}")
            flash('❌ Gagal mengunggah file bukti. Pastikan format file benar.', 'danger')
            return redirect(url_for('main.request_account'))
            
        # 2. Simpan data ke tabel pending_users dengan URL file
        pending_user = PendingUser(
            nim=form.nim.data,
            nama_lengkap=form.nama_lengkap.data,
            prodi=form.prodi.data,
            email=form.email.data,
            hp=form.hp.data,
            bukti_url=bukti_url, # <-- Menggunakan URL file yang sudah disimpan
            status='pending'
        )
        
        db.session.add(pending_user)
        db.session.commit()
        
        flash('Permintaan Akun Anda berhasil diajukan. Kami akan segera memverifikasinya. Status akan dikirim via Email.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('request_account.html', title='Ajukan Akun', form=form)

# --- Contoh Halaman yang Dilindungi (Wajib Login) ---
@main.route('/profile')
@login_required 
def profile():
    return f"Halo, {current_user.nama_lengkap} ({current_user.role})! Anda sudah login."