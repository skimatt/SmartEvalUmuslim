from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from flask_wtf.file import FileField, FileAllowed    # <-- ini yang benar
from models import Report, Rating, Lecturer
from app import proofs

# --- 1. Form Membuat Laporan Baru ---
class ReportForm(FlaskForm):
    judul = StringField('Judul Laporan', validators=[
        DataRequired(message='Judul wajib diisi.'), 
        Length(min=5, max=100, message='Judul harus antara 5 hingga 100 karakter.')
    ])
    
    kategori = SelectField('Kategori Laporan', choices=[
        ('Fasilitas', 'Fasilitas Kampus (Toilet, AC, Gedung, dll.)'),
        ('Layanan TU', 'Layanan Tata Usaha & Administrasi'),
        ('Perpustakaan', 'Layanan & Koleksi Perpustakaan'),
        ('Akademik', 'Masalah terkait Kurikulum & Jadwal'),
        ('Lainnya', 'Lainnya (Tulis di deskripsi)')
    ], validators=[DataRequired()])
    
    deskripsi = TextAreaField('Deskripsi Lengkap', validators=[
        DataRequired(message='Deskripsi lengkap wajib diisi.'), 
        Length(min=20, message='Deskripsi minimal 20 karakter.')
    ])
    
    # --- FIELD UPLOAD BUKTI LAPORAN (OPSIONAL) ---
    bukti_laporan = FileField('Lampirkan Bukti (Opsional)', validators=[
        Optional(), # Tidak wajib diisi
        FileAllowed(proofs, 'Hanya perbolehkan file gambar (jpg, jpeg, png, gif)')
    ])
    # ----------------------------------------------
    
    submit = SubmitField('Kirim Laporan')

# --- 2. Form Memberi Penilaian Dosen ---
class RatingForm(FlaskForm):
    # ... (kode rating form sama)
    lecturer_id = HiddenField()
    rating_mengajar = SelectField('1. Cara Mengajar (1-5)', choices=[(str(i), str(i)) for i in range(1, 6)], validators=[DataRequired()])
    rating_tugas = SelectField('2. Penilaian Tugas (1-5)', choices=[(str(i), str(i)) for i in range(1, 6)], validators=[DataRequired()])
    rating_materi = SelectField('3. Penguasaan Materi (1-5)', choices=[(str(i), str(i)) for i in range(1, 6)], validators=[DataRequired()])
    komentar = TextAreaField('Komentar Singkat (Opsional)', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Kirim Penilaian')