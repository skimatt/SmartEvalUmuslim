from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_wtf.file import FileRequired, FileAllowed
from models import User, PendingUser # Import Model untuk validasi
from app import proofs # Import UploadSet proofs dari app.py

# Form Login
class LoginForm(FlaskForm):
    username = StringField('Username (NIM/Email)', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Form Pengajuan Akun (Mahasiswa)
class RequestAccountForm(FlaskForm):
    nama_lengkap = StringField('Nama Lengkap', validators=[DataRequired(), Length(min=3, max=150)])
    nim = StringField('NIM', validators=[DataRequired(), Length(min=10, max=15)])
    
    prodi = SelectField('Program Studi', choices=[
        ('TI', 'Teknik Informatika'),
        ('SI', 'Sistem Informasi'),
        ('MN', 'Manajemen'),
        ('AK', 'Akuntansi'),
        ('HK', 'Hukum'),
        ('Lain', 'Lainnya')
    ], validators=[DataRequired()])
    
    email = StringField('Email Kampus/Personal', validators=[DataRequired(), Email()])
    hp = StringField('No. HP', validators=[DataRequired(), Length(min=10, max=15)])
    
    # --- FIELD BARU UNTUK UPLOAD FILE ---
    bukti_upload = FileField('Upload Bukti (KTM/KRS)', validators=[
        FileRequired('Wajib melampirkan bukti KTM atau KRS.'),
        FileAllowed(proofs, 'Hanya perbolehkan file gambar (jpg, jpeg, png, gif)')
    ])
    # ------------------------------------
    
    submit = SubmitField('Ajukan Akun')

    # Validasi kustom untuk memastikan NIM belum terdaftar
    def validate_nim(self, nim):
        if User.query.filter_by(nim=nim.data).first():
            raise ValidationError('NIM ini sudah memiliki akun terdaftar.')
        pending = PendingUser.query.filter_by(nim=nim.data).first()
        if pending and pending.status == 'pending':
            raise ValidationError('NIM ini sedang dalam proses verifikasi. Mohon tunggu kabar dari Admin.')