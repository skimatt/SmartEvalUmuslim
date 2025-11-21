import os
import logging
from flask import Flask, redirect, url_for, Blueprint 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES # <-- PENTING

# --- INISIALISASI EKSTENSI ---
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Konfigurasi UploadSet untuk file bukti (KTM/KRS)
proofs = UploadSet('proofs', IMAGES) 

login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'

def create_app():
    # Inisialisasi aplikasi Flask
    app = Flask(__name__)
    
    # Kunci Rahasia Wajib
    app.config['SECRET_KEY'] = 'kunci_rahasia_final_project_smarteval_umu_12345'
    app.config['DEBUG'] = True 

    # --- KONFIGURASI DATABASE ---
    DB_USER = 'root'
    DB_PASSWORD = '' 
    DB_HOST = 'localhost'
    DB_PORT = 3306 
    DB_NAME = 'smart_eval_umu' 

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # --- KONFIGURASI UPLOAD FILE (PERBAIKAN URL) ---
    # Direktori penyimpanan fisik
    app.config['UPLOADED_PROOFS_DEST'] = os.path.join(app.root_path, 'uploads/proofs') 
    # URL Publik tempat file disajikan (misal: http://127.0.0.1:5000/uploads/proofs/)
    app.config['UPLOADED_PROOFS_URL'] = '/uploads/proofs/' 
    
    configure_uploads(app, (proofs,)) 
    # -----------------------------------------------
    
    # --- KONFIGURASI LOGGING ---
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = logging.FileHandler('logs/smarteval.log', encoding='utf-8') 
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('SmartEval Startup') 

    # Inisialisasi ekstensi dengan konfigurasi aplikasi
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # --- REGISTRASI BLUEPRINT ---
    from main.routes import main as main_blueprint
    from admin.routes import admin as admin_blueprint 
    from mahasiswa.routes import mahasiswa as mahasiswa_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(mahasiswa_blueprint, url_prefix='/mahasiswa')
    
    return app